#!/usr/bin/env python3
"""
Verification script for DApp Voting System infrastructure setup.
Checks all required services and dependencies.
"""
import sys
import subprocess
import asyncio
from typing import Tuple, List


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_check(name: str, status: bool, message: str = ""):
    """Print check result"""
    symbol = f"{Colors.GREEN}✓{Colors.END}" if status else f"{Colors.RED}✗{Colors.END}"
    status_text = f"{Colors.GREEN}OK{Colors.END}" if status else f"{Colors.RED}FAIL{Colors.END}"
    print(f"{symbol} {name:.<50} {status_text}")
    if message:
        print(f"  {Colors.YELLOW}→ {message}{Colors.END}")


def check_command(command: str) -> Tuple[bool, str]:
    """Check if command exists"""
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return True, result.stdout.split('\n')[0]
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        return False, "Not found"


def check_python_version() -> Tuple[bool, str]:
    """Check Python version"""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    is_valid = version.major == 3 and version.minor >= 10
    return is_valid, version_str


def check_python_package(package: str) -> Tuple[bool, str]:
    """Check if Python package is installed"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    return True, line.split(':')[1].strip()
        return False, "Not installed"
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        return False, "Error checking"


async def check_postgres_async() -> Tuple[bool, str]:
    """Check PostgreSQL connection"""
    try:
        from app.database import engine
        async with engine.begin() as conn:
            result = await conn.execute("SELECT version()")
            version = result.scalar()
            return True, version.split(',')[0]
    except Exception as e:
        return False, str(e)


async def check_redis_async() -> Tuple[bool, str]:
    """Check Redis connection"""
    try:
        from app.redis_client import redis_client
        await redis_client.connect()
        info = await redis_client.redis.info()
        version = info.get('redis_version', 'unknown')
        await redis_client.close()
        return True, f"Redis {version}"
    except Exception as e:
        return False, str(e)


def check_docker_service(service: str) -> Tuple[bool, str]:
    """Check if Docker service is running"""
    try:
        result = subprocess.run(
            ["docker-compose", "ps", service],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "Up" in result.stdout:
            return True, "Running"
        return False, "Not running"
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        return False, "Docker Compose not available"


def main():
    """Main verification function"""
    print(f"\n{Colors.BOLD}DApp Voting System - Infrastructure Verification{Colors.END}")
    print(f"{Colors.BOLD}Version 2.0.0{Colors.END}")
    
    all_checks_passed = True
    
    # Check system commands
    print_header("System Commands")
    
    checks = [
        ("Python", "python3"),
        ("Docker", "docker"),
        ("Docker Compose", "docker-compose"),
        ("Git", "git"),
    ]
    
    for name, command in checks:
        status, message = check_command(command)
        print_check(name, status, message)
        all_checks_passed = all_checks_passed and status
    
    # Check Python version
    print_header("Python Environment")
    
    status, version = check_python_version()
    print_check("Python 3.10+", status, f"Version: {version}")
    all_checks_passed = all_checks_passed and status
    
    # Check critical Python packages
    print_header("Python Packages")
    
    packages = [
        ("FastAPI", "fastapi"),
        ("SQLAlchemy", "sqlalchemy"),
        ("Redis", "redis"),
        ("Celery", "celery"),
        ("Cryptography", "cryptography"),
        ("Paillier", "phe"),
        ("PyOTP", "pyotp"),
        ("TensorFlow", "tensorflow"),
        ("Scikit-learn", "sklearn"),
        ("OpenCV", "cv2"),
    ]
    
    for name, package in packages:
        status, message = check_python_package(package)
        print_check(name, status, message)
        if not status:
            all_checks_passed = False
    
    # Check Docker services
    print_header("Docker Services")
    
    services = [
        ("PostgreSQL", "postgres"),
        ("Redis", "redis"),
        ("MinIO", "minio"),
        ("Backend", "backend"),
    ]
    
    for name, service in services:
        status, message = check_docker_service(service)
        print_check(name, status, message)
        # Don't fail if Docker services aren't running (might be manual setup)
    
    # Check database and Redis connections
    print_header("Service Connections")
    
    try:
        # Check PostgreSQL
        status, message = asyncio.run(check_postgres_async())
        print_check("PostgreSQL Connection", status, message)
        all_checks_passed = all_checks_passed and status
    except Exception as e:
        print_check("PostgreSQL Connection", False, str(e))
        all_checks_passed = False
    
    try:
        # Check Redis
        status, message = asyncio.run(check_redis_async())
        print_check("Redis Connection", status, message)
        all_checks_passed = all_checks_passed and status
    except Exception as e:
        print_check("Redis Connection", False, str(e))
        all_checks_passed = False
    
    # Check configuration files
    print_header("Configuration Files")
    
    import os
    config_files = [
        (".env", ".env"),
        ("Docker Compose", "docker-compose.yml"),
        ("Requirements", "requirements-upgrade.txt"),
        ("Alembic Config", "backend/alembic.ini"),
    ]
    
    for name, filepath in config_files:
        exists = os.path.exists(filepath)
        print_check(name, exists, filepath)
        all_checks_passed = all_checks_passed and exists
    
    # Final summary
    print_header("Verification Summary")
    
    if all_checks_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All checks passed!{Colors.END}")
        print(f"\n{Colors.GREEN}Infrastructure is ready for development.{Colors.END}")
        print(f"\nNext steps:")
        print(f"  1. Start services: docker-compose up -d")
        print(f"  2. Run migrations: docker-compose exec backend alembic upgrade head")
        print(f"  3. Access API docs: http://localhost:8000/api/docs")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Some checks failed!{Colors.END}")
        print(f"\n{Colors.YELLOW}Please review the errors above and:{Colors.END}")
        print(f"  1. Install missing dependencies")
        print(f"  2. Start required services")
        print(f"  3. Check configuration files")
        print(f"  4. Run this script again")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Verification cancelled by user.{Colors.END}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")
        sys.exit(1)
