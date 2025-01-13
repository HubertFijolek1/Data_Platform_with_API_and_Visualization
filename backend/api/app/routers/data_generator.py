import logging
import os
import re
from typing import Callable, Dict, List

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import SessionLocal
from ..utils.generators import (
    generate_account_number,
    generate_admission_date,
    generate_age,
    generate_amount,
    generate_assigned_agent,
    generate_attendance_rate,
    generate_balance,
    generate_battery_level,
    generate_branch,
    generate_brand,
    generate_category,
    generate_channel,
    generate_class_field,
    generate_comments,
    generate_company_name,
    generate_content_type,
    generate_country,
    generate_created_at,
    generate_creation_date,
    generate_currency,
    generate_customer_name,
    generate_delivery_status,
    generate_device_name,
    generate_diagnosis,
    generate_discharge_date,
    generate_dividend_yield,
    generate_doctor_id,
    generate_email,
    generate_engagement_rate,
    generate_exam_score,
    generate_extra_curricular,
    generate_gender,
    generate_generic,
    generate_generic_id,
    generate_grade,
    generate_hashtags,
    generate_helpful_votes,
    generate_high,
    generate_humidity,
    generate_ifsc_code,
    generate_insurance_status,
    generate_is_fraud,
    generate_issue_type,
    generate_last_login,
    generate_light_intensity,
    generate_likes,
    generate_low,
    generate_market_cap,
    generate_motion_detected,
    generate_name,
    generate_patient_id,
    generate_payment_method,
    generate_pe_ratio,
    generate_platform,
    generate_post_id,
    generate_pressure,
    generate_price_close,
    generate_price_open,
    generate_priority,
    generate_product_id,
    generate_quantity,
    generate_rating,
    generate_resolution_date,
    generate_review_id,
    generate_review_text,
    generate_satisfaction_rating,
    generate_sensor_id,
    generate_shares,
    generate_sign_up_date,
    generate_status,
    generate_student_id,
    generate_subject,
    generate_subscription_plan,
    generate_temperature,
    generate_ticker,
    generate_ticket_id,
    generate_timestamp,
    generate_transaction_id,
    generate_transaction_type,
    generate_treatment,
    generate_user_id,
    generate_verified_purchase,
    generate_volume,
)
from ..utils.role_checker import RoleChecker

router = APIRouter(
    prefix="/data-generator",
    tags=["data-generator"],
)

logger = logging.getLogger("app")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Utility function to sanitize filenames
def sanitize_filename(name: str) -> str:
    return re.sub(r"[^\w\-\.]", "_", name)


class GenerateDatasetRequest(BaseModel):
    """
    Pydantic model for handling dataset generation requests.
    """

    n_rows: int = Field(
        ..., ge=100, le=100000, description="Number of rows (min: 100, max: 100,000)"
    )
    columns: List[str] = Field(
        ..., description="List of columns to include in the dataset"
    )
    dataset_name: str = Field(..., description="Name of the dataset")
    filename: str | None = Field(
        default=None, description="Optional custom file name (e.g., 'MyData.csv')"
    )
    overwrite: bool = Field(
        default=False, description="If True and filename already exists, overwrite it"
    )


# Mapping of column names to their respective generator functions
COLUMN_GENERATORS: Dict[str, Callable[[int], List]] = {
    "user_id": generate_user_id,
    "transaction_id": generate_transaction_id,
    "product_id": generate_product_id,
    "patient_id": generate_patient_id,
    "account_number": generate_account_number,
    "student_id": generate_student_id,
    "review_id": generate_review_id,
    "sensor_id": generate_sensor_id,
    "ticket_id": generate_ticket_id,
    "ticker": generate_ticker,
    "post_id": generate_post_id,
    "name": generate_name,
    "email": generate_email,
    "age": generate_age,
    "gender": generate_gender,
    "country": generate_country,
    "sign_up_date": generate_sign_up_date,
    "created_at": generate_created_at,
    "subscription_plan": generate_subscription_plan,
    "status": generate_status,
    "last_login": generate_last_login,
    "category": generate_category,
    "amount": generate_amount,
    "currency": generate_currency,
    "timestamp": generate_timestamp,
    "quantity": generate_quantity,
    "payment_method": generate_payment_method,
    "delivery_status": generate_delivery_status,
    "diagnosis": generate_diagnosis,
    "treatment": generate_treatment,
    "admission_date": generate_admission_date,
    "discharge_date": generate_discharge_date,
    "doctor_id": generate_doctor_id,
    "insurance_status": generate_insurance_status,
    "customer_name": generate_customer_name,
    "balance": generate_balance,
    "transaction_type": generate_transaction_type,
    "branch": generate_branch,
    "ifsc_code": generate_ifsc_code,
    "is_fraud": generate_is_fraud,
    "grade": generate_grade,
    "class": generate_class_field,
    "subject": generate_subject,
    "attendance_rate": generate_attendance_rate,
    "exam_score": generate_exam_score,
    "extra_curricular": generate_extra_curricular,
    "rating": generate_rating,
    "review_text": generate_review_text,
    "helpful_votes": generate_helpful_votes,
    "verified_purchase": generate_verified_purchase,
    "brand": generate_brand,
    "device_name": generate_device_name,
    "temperature": generate_temperature,
    "humidity": generate_humidity,
    "pressure": generate_pressure,
    "light_intensity": generate_light_intensity,
    "motion_detected": generate_motion_detected,
    "battery_level": generate_battery_level,
    "issue_type": generate_issue_type,
    "priority": generate_priority,
    "creation_date": generate_creation_date,
    "resolution_date": generate_resolution_date,
    "assigned_agent": generate_assigned_agent,
    "channel": generate_channel,
    "satisfaction_rating": generate_satisfaction_rating,
    "company_name": generate_company_name,
    "price_open": generate_price_open,
    "price_close": generate_price_close,
    "high": generate_high,
    "low": generate_low,
    "volume": generate_volume,
    "market_cap": generate_market_cap,
    "pe_ratio": generate_pe_ratio,
    "dividend_yield": generate_dividend_yield,
    "platform": generate_platform,
    "content_type": generate_content_type,
    "likes": generate_likes,
    "shares": generate_shares,
    "comments": generate_comments,
    "engagement_rate": generate_engagement_rate,
    "hashtags": generate_hashtags,
}


@router.post(
    "/generate",
    response_model=schemas.DatasetRead,
    dependencies=[Depends(RoleChecker(["admin", "user"]))],
)
def generate_dataset(request: GenerateDatasetRequest, db: Session = Depends(get_db)):
    n_rows = request.n_rows
    selected_columns = request.columns
    dataset_name = request.dataset_name.strip()

    filename_input = (
        request.filename.strip() if request.filename else None
    )  # may be None or user-supplied
    overwrite = request.overwrite

    # Step 1: Generate the data in memory
    data = {}
    for column in selected_columns:
        generator_func = COLUMN_GENERATORS.get(column)
        if not generator_func:
            data[column] = generate_generic(column, n_rows)
        else:
            try:
                data[column] = generator_func(n_rows)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error generating data for column '{column}': {str(e)}",
                )
    df = pd.DataFrame(data)

    # Step 2: Determine the final file name
    if filename_input:
        # Ensure the filename has a .csv extension
        if not filename_input.lower().endswith(".csv"):
            filename_input += ".csv"
        final_file_name = sanitize_filename(filename_input)
    else:
        # Default to dataset_name with .csv extension
        sanitized_name = sanitize_filename(dataset_name)
        final_file_name = f"{sanitized_name}.csv"

    if not final_file_name:
        final_file_name = f"{sanitize_filename(dataset_name)}.csv"

    # Step 3: Check for file existence
    uploads_dir = os.path.join(os.getcwd(), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, final_file_name)

    if os.path.exists(file_path):
        if not overwrite:
            raise HTTPException(
                status_code=409,
                detail=f"File '{final_file_name}' already exists. "
                f"Please use overwrite=true or provide a different filename.",
            )
        else:
            # Overwrite: remove old file
            try:
                os.remove(file_path)
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to overwrite existing file '{final_file_name}': {str(e)}",
                )

    # Step 4: Save the CSV to disk
    try:
        df.to_csv(file_path, index=False)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to save dataset to disk: {str(e)}"
        )

    # Step 5: Create a dataset entry in the database
    dataset = models.Dataset(
        name=dataset_name,
        file_name=final_file_name,
        uploaded_at=pd.Timestamp.utcnow(),
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return dataset
