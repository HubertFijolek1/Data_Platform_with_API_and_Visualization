from faker import Faker
import pandas as pd
import os
import argparse
import uuid


def generate_users(n=100):
    fake = Faker()
    users = []
    for _ in range(n):
        users.append({
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password(length=12)
        })
    return pd.DataFrame(users)


def generate_datasets(n=50):
    fake = Faker()
    datasets = []
    for i in range(n):
        datasets.append({
            "name": f"Dataset_{i}",
            "file_name": f"dataset_{i}.csv",
            "uploaded_at": fake.date_time_this_year()
        })
    return pd.DataFrame(datasets)


def save_to_csv(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic data for the platform.")
    parser.add_argument('--users', type=int, default=100, help='Number of users to generate.')
    parser.add_argument('--datasets', type=int, default=50, help='Number of datasets to generate.')
    args = parser.parse_args()

    users_df = generate_users(args.users)
    datasets_df = generate_datasets(args.datasets)

    save_to_csv(users_df, os.path.join("backend", "sample_data", "users.csv"))
    save_to_csv(datasets_df, os.path.join("backend", "sample_data", "datasets.csv"))

    print(f"Generated {args.users} users and {args.datasets} datasets successfully.")


if __name__ == "__main__":
    main()