import random
from typing import List

from faker import Faker

fake = Faker()


def generate_user_id(n_rows: int) -> List[str]:
    return [fake.unique.uuid4() for _ in range(n_rows)]


def generate_transaction_id(n_rows: int) -> List[str]:
    return [fake.unique.uuid4() for _ in range(n_rows)]


def generate_product_id(n_rows: int) -> List[str]:
    return [fake.unique.uuid4() for _ in range(n_rows)]


def generate_patient_id(n_rows: int) -> List[str]:
    return [fake.unique.uuid4() for _ in range(n_rows)]


def generate_account_number(n_rows: int) -> List[str]:
    return [fake.unique.bban() for _ in range(n_rows)]


def generate_student_id(n_rows: int) -> List[str]:
    return [fake.unique.bothify(text="??####") for _ in range(n_rows)]


def generate_review_id(n_rows: int) -> List[str]:
    return [fake.unique.uuid4() for _ in range(n_rows)]


def generate_sensor_id(n_rows: int) -> List[str]:
    return [fake.unique.uuid4() for _ in range(n_rows)]


def generate_ticket_id(n_rows: int) -> List[str]:
    return [fake.unique.uuid4() for _ in range(n_rows)]


def generate_ticker(n_rows: int) -> List[str]:
    return [fake.stock_symbol() for _ in range(n_rows)]


def generate_post_id(n_rows: int) -> List[str]:
    return [fake.unique.uuid4() for _ in range(n_rows)]


def generate_generic_id(n_rows: int) -> List[str]:
    return [fake.unique.uuid4() for _ in range(n_rows)]


def generate_name(n_rows: int) -> List[str]:
    return [fake.name() for _ in range(n_rows)]


def generate_email(n_rows: int) -> List[str]:
    return [fake.email() for _ in range(n_rows)]


def generate_age(n_rows: int) -> List[int]:
    return [random.randint(18, 80) for _ in range(n_rows)]


def generate_gender(n_rows: int) -> List[str]:
    return [random.choice(["Male", "Female", "Other"]) for _ in range(n_rows)]


def generate_country(n_rows: int) -> List[str]:
    return [fake.country() for _ in range(n_rows)]


def generate_sign_up_date(n_rows: int) -> List[str]:
    return [fake.date_this_decade().isoformat() for _ in range(n_rows)]


def generate_created_at(n_rows: int) -> List[str]:
    return [fake.date_time_this_decade().isoformat() for _ in range(n_rows)]


def generate_subscription_plan(n_rows: int) -> List[str]:
    return [
        random.choice(["Free", "Basic", "Premium", "Enterprise"]) for _ in range(n_rows)
    ]


def generate_status(n_rows: int) -> List[str]:
    return [
        random.choice(["Active", "Inactive", "Pending", "Banned"])
        for _ in range(n_rows)
    ]


def generate_last_login(n_rows: int) -> List[str]:
    return [fake.date_time_this_year().isoformat() for _ in range(n_rows)]


def generate_category(n_rows: int) -> List[str]:
    return [fake.word() for _ in range(n_rows)]


def generate_amount(n_rows: int) -> List[float]:
    return [round(random.uniform(10, 999), 2) for _ in range(n_rows)]


def generate_currency(n_rows: int) -> List[str]:
    return [random.choice(["USD", "EUR", "GBP", "JPY", "INR"]) for _ in range(n_rows)]


def generate_timestamp(n_rows: int) -> List[str]:
    return [fake.date_time_this_year().isoformat() for _ in range(n_rows)]


def generate_quantity(n_rows: int) -> List[int]:
    return [random.randint(1, 10) for _ in range(n_rows)]


def generate_payment_method(n_rows: int) -> List[str]:
    return [
        random.choice(["Credit Card", "PayPal", "Bank Transfer", "Cash"])
        for _ in range(n_rows)
    ]


def generate_delivery_status(n_rows: int) -> List[str]:
    return [
        random.choice(["Pending", "Shipped", "Delivered", "Returned"])
        for _ in range(n_rows)
    ]


def generate_diagnosis(n_rows: int) -> List[str]:
    return [
        random.choice(["Flu", "Diabetes", "Hypertension", "Cancer", "Healthy"])
        for _ in range(n_rows)
    ]


def generate_treatment(n_rows: int) -> List[str]:
    return [
        random.choice(["Medication", "Surgery", "Therapy", "Observation"])
        for _ in range(n_rows)
    ]


def generate_admission_date(n_rows: int) -> List[str]:
    return [fake.date_this_year().isoformat() for _ in range(n_rows)]


def generate_discharge_date(n_rows: int) -> List[str]:
    return [fake.date_this_year().isoformat() for _ in range(n_rows)]


def generate_doctor_id(n_rows: int) -> List[int]:
    return [random.randint(100, 999) for _ in range(n_rows)]


def generate_insurance_status(n_rows: int) -> List[str]:
    return [random.choice(["Insured", "Uninsured", "Pending"]) for _ in range(n_rows)]


def generate_customer_name(n_rows: int) -> List[str]:
    return [fake.name() for _ in range(n_rows)]


def generate_balance(n_rows: int) -> List[float]:
    return [round(random.uniform(100, 100000), 2) for _ in range(n_rows)]


def generate_transaction_type(n_rows: int) -> List[str]:
    return [random.choice(["Deposit", "Withdrawal", "Transfer"]) for _ in range(n_rows)]


def generate_branch(n_rows: int) -> List[str]:
    return [fake.city() for _ in range(n_rows)]


def generate_ifsc_code(n_rows: int) -> List[str]:
    return [fake.bban() for _ in range(n_rows)]


def generate_is_fraud(n_rows: int) -> List[bool]:
    return [random.choice([True, False]) for _ in range(n_rows)]


def generate_grade(n_rows: int) -> List[str]:
    return [random.choice(["A", "B", "C", "D", "F"]) for _ in range(n_rows)]


def generate_class_field(n_rows: int) -> List[str]:
    return [random.choice(["Class 1", "Class 2", "Class 3"]) for _ in range(n_rows)]


def generate_subject(n_rows: int) -> List[str]:
    return [
        random.choice(["Math", "Science", "History", "Language"]) for _ in range(n_rows)
    ]


def generate_attendance_rate(n_rows: int) -> List[float]:
    return [round(random.uniform(0, 100), 2) for _ in range(n_rows)]


def generate_exam_score(n_rows: int) -> List[int]:
    return [random.randint(0, 100) for _ in range(n_rows)]


def generate_extra_curricular(n_rows: int) -> List[str]:
    return [
        random.choice(["Sports", "Music", "Art", "Volunteering", "None"])
        for _ in range(n_rows)
    ]


def generate_rating(n_rows: int) -> List[int]:
    return [random.randint(1, 5) for _ in range(n_rows)]


def generate_review_text(n_rows: int) -> List[str]:
    return [fake.text(max_nb_chars=100) for _ in range(n_rows)]


def generate_helpful_votes(n_rows: int) -> List[int]:
    return [random.randint(0, 1000) for _ in range(n_rows)]


def generate_verified_purchase(n_rows: int) -> List[bool]:
    return [random.choice([True, False]) for _ in range(n_rows)]


def generate_brand(n_rows: int) -> List[str]:
    return [fake.company() for _ in range(n_rows)]


def generate_device_name(n_rows: int) -> List[str]:
    return [fake.word().title() for _ in range(n_rows)]


def generate_temperature(n_rows: int) -> List[float]:
    return [round(random.uniform(-10, 40), 2) for _ in range(n_rows)]


def generate_humidity(n_rows: int) -> List[float]:
    return [round(random.uniform(0, 100), 2) for _ in range(n_rows)]


def generate_pressure(n_rows: int) -> List[float]:
    return [round(random.uniform(950, 1050), 2) for _ in range(n_rows)]


def generate_light_intensity(n_rows: int) -> List[int]:
    return [random.randint(0, 10000) for _ in range(n_rows)]


def generate_motion_detected(n_rows: int) -> List[bool]:
    return [random.choice([True, False]) for _ in range(n_rows)]


def generate_battery_level(n_rows: int) -> List[float]:
    return [round(random.uniform(0, 100), 2) for _ in range(n_rows)]


def generate_issue_type(n_rows: int) -> List[str]:
    return [
        random.choice(
            ["Login Issue", "Payment Failure", "Bug Report", "Feature Request"]
        )
        for _ in range(n_rows)
    ]


def generate_priority(n_rows: int) -> List[str]:
    return [random.choice(["Low", "Medium", "High"]) for _ in range(n_rows)]


def generate_creation_date(n_rows: int) -> List[str]:
    return [fake.date_time_this_month().isoformat() for _ in range(n_rows)]


def generate_resolution_date(n_rows: int) -> List[str]:
    return [fake.date_time_this_month().isoformat() for _ in range(n_rows)]


def generate_assigned_agent(n_rows: int) -> List[str]:
    return [fake.name() for _ in range(n_rows)]


def generate_channel(n_rows: int) -> List[str]:
    return [
        random.choice(["Email", "Phone", "Chat", "Social Media"]) for _ in range(n_rows)
    ]


def generate_satisfaction_rating(n_rows: int) -> List[int]:
    return [random.randint(1, 5) for _ in range(n_rows)]


def generate_company_name(n_rows: int) -> List[str]:
    return [fake.company() for _ in range(n_rows)]


def generate_price_open(n_rows: int) -> List[float]:
    return [round(random.uniform(10, 500), 2) for _ in range(n_rows)]


def generate_price_close(n_rows: int) -> List[float]:
    return [round(random.uniform(10, 500), 2) for _ in range(n_rows)]


def generate_high(n_rows: int) -> List[float]:
    return [round(random.uniform(10, 600), 2) for _ in range(n_rows)]


def generate_low(n_rows: int) -> List[float]:
    return [round(random.uniform(10, 400), 2) for _ in range(n_rows)]


def generate_volume(n_rows: int) -> List[int]:
    return [random.randint(10000, 10000000) for _ in range(n_rows)]


def generate_market_cap(n_rows: int) -> List[float]:
    return [round(random.uniform(1e6, 1e9), 2) for _ in range(n_rows)]


def generate_pe_ratio(n_rows: int) -> List[float]:
    return [round(random.uniform(1, 50), 2) for _ in range(n_rows)]


def generate_dividend_yield(n_rows: int) -> List[float]:
    return [round(random.uniform(0, 5), 2) for _ in range(n_rows)]


def generate_platform(n_rows: int) -> List[str]:
    return [
        random.choice(["Facebook", "Twitter", "Instagram", "LinkedIn"])
        for _ in range(n_rows)
    ]


def generate_content_type(n_rows: int) -> List[str]:
    return [random.choice(["Text", "Image", "Video", "Link"]) for _ in range(n_rows)]


def generate_likes(n_rows: int) -> List[int]:
    return [random.randint(0, 10000) for _ in range(n_rows)]


def generate_shares(n_rows: int) -> List[int]:
    return [random.randint(0, 10000) for _ in range(n_rows)]


def generate_comments(n_rows: int) -> List[int]:
    return [random.randint(0, 10000) for _ in range(n_rows)]


def generate_engagement_rate(n_rows: int) -> List[float]:
    return [round(random.uniform(0, 10), 2) for _ in range(n_rows)]


def generate_hashtags(n_rows: int) -> List[str]:
    return [f"#{fake.word()}" for _ in range(n_rows)]


def generate_generic(column_name: str, n_rows: int) -> List[str]:
    return [fake.word() for _ in range(n_rows)]
