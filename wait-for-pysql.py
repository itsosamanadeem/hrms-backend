import argparse
import psycopg2
import sys
import os
import time

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--db_host', default=os.getenv("DB_HOST", "localhost"))
    arg_parser.add_argument('--db_port', type=int, default=os.getenv("DB_PORT", 5432))
    arg_parser.add_argument('--db_user', default=os.getenv("DB_USER", "postgres"))
    arg_parser.add_argument('--db_password', default=os.getenv("DB_PASSWORD", 'supersecret'))
    arg_parser.add_argument('--db_name', default=os.getenv("DB_NAME",'postgres'))
    arg_parser.add_argument('--timeout', type=int, default=30)

    args = arg_parser.parse_args()

    print(f"Waiting for database {args.db_name} at {args.db_host}:{args.db_port} as user {args.db_user}..., password {args.db_password}")
    
    start_time = time.time()
    error = None
    while (time.time() - start_time) < args.timeout:
        try:
            conn = psycopg2.connect(
                user=args.db_user,
                password=args.db_password,
                host=args.db_host,
                port=args.db_port,
                dbname=args.db_name  
            )
            conn.close()
            error = None
            print("✅ PostgreSQL is ready!")
            break
        except psycopg2.OperationalError as e:
            error = e
            time.sleep(1)

    if error:
        print(f"❌ Database connection failure: {error}", file=sys.stderr)
        sys.exit(1)
