#!/usr/bin/env python3
"""
Simple script to reset admin password
Usage: python reset_admin_password.py
"""
import os
import sys
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User

def reset_password(username, new_password):
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"❌ User '{username}' not found!")
            return False
        
        user.password = generate_password_hash(new_password)
        db.session.commit()
        print(f"✅ Password reset successful for user: {username}")
        print(f"📧 Email: {user.email}")
        print(f"👤 Role: {user.role}")
        print(f"\n🔑 New password: {new_password}")
        print(f"\nYou can now login with:")
        print(f"   Username: {username}")
        print(f"   Password: {new_password}")
        return True

if __name__ == "__main__":
    print("=" * 50)
    print("🔐 Admin Password Reset Tool")
    print("=" * 50)
    
    username = input("\nEnter username (default: Mouktik): ").strip() or "Mouktik"
    new_password = input("Enter new password (default: admin123): ").strip() or "admin123"
    
    print("\n⏳ Resetting password...")
    reset_password(username, new_password)
    print("\n" + "=" * 50)
