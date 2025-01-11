import logging
import os
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


class GenerateDatasetRequest(BaseModel):
    """
    Pydantic model for handling dataset generation requests.
    """

    n_rows: int = Field(..., gt=0, le=10000, description="Number of rows (max: 10,000)")
    columns: List[str] = Field(
        ..., description="List of columns to include in the dataset"
    )
    dataset_name: str = Field(..., description="Name of the dataset")


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
    """
    Generate a synthetic dataset based on selected columns and number of rows.
    """
    n_rows = request.n_rows
    selected_columns = request.columns
    dataset_name = request.dataset_name

    logger.debug(
        f"Generating synthetic dataset '{dataset_name}' with {n_rows} rows for columns: {selected_columns}"
    )

    # Generate the data
    data = {}
    for column in selected_columns:
        generator_func = COLUMN_GENERATORS.get(column)
        if not generator_func:
            logger.warning(
                f"No generator found for column '{column}'. Using generic generator."
            )
            data[column] = generate_generic(column, n_rows)
            continue
        try:
            data[column] = generator_func(n_rows)
        except Exception as e:
            logger.error(f"Error generating data for column '{column}': {e}")
            raise HTTPException(
                status_code=400, detail=f"Error generating data for column '{column}'."
            )

    df = pd.DataFrame(data)

    # Create a dataset entry
    dataset = models.Dataset(
        name=dataset_name,
        file_name="",  # Placeholder
        uploaded_at=pd.Timestamp.utcnow(),
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    # Create and save the CSV file
    file_name = f"generated_{dataset.id}.csv"
    uploads_dir = os.path.join(os.getcwd(), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, file_name)
    df.to_csv(file_path, index=False)

    # Update the dataset metadata
    dataset.file_name = file_name
    db.commit()
    db.refresh(dataset)

    logger.info(
        f"Synthetic dataset '{dataset_name}' generated and saved as {file_name}."
    )

    return dataset
