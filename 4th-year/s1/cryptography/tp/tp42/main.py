#!/usr/bin/env python3
"""
File Encryption/Decryption CLI
Main interface for the encryption system
"""

import os
import sys
from encryption import FileEncryptor
from getpass import getpass


def print_banner():
    """Print application banner"""
    print("=" * 60)
    print(" " * 10 + "FILE ENCRYPTION/DECRYPTION SYSTEM")
    print(" " * 15 + "Using BLAKE2s + HMAC + AES")
    print("=" * 60)
    print()


def print_menu():
    """Print main menu"""
    print("\n" + "─" * 60)
    print("MAIN MENU")
    print("─" * 60)
    print("1. Encrypt a file")
    print("2. Decrypt a file")
    print("3. Exit")
    print("─" * 60)


def get_file_path(prompt, must_exist=True):
    """Get and validate file path from user"""
    while True:
        path = input(prompt).strip()
        if not path:
            print("⚠ Error: Path cannot be empty")
            continue
        
        if must_exist and not os.path.exists(path):
            print(f"⚠ Error: File '{path}' does not exist")
            continue
        
        if must_exist and not os.path.isfile(path):
            print(f"⚠ Error: '{path}' is not a file")
            continue
        
        return path


def encrypt_file_ui():
    """User interface for file encryption"""
    print("\n" + "═" * 60)
    print(" " * 20 + "FILE ENCRYPTION")
    print("═" * 60)
    
    # Get input file
    input_file = get_file_path("\n📁 Enter the path of the file to encrypt: ", must_exist=True)
    
    # Get encryption mode
    print("\n🔐 Select encryption mode:")
    print("  1. CBC (Cipher Block Chaining)")
    print("  2. CTR (Counter Mode)")
    
    while True:
        mode_choice = input("\nEnter your choice (1 or 2): ").strip()
        if mode_choice in ['1', '2']:
            break
        print("⚠ Invalid choice. Please enter 1 or 2.")
    
    mode = 'CBC' if mode_choice == '1' else 'CTR'
    
    # Get password
    while True:
        password = getpass("\n🔑 Enter encryption password: ")
        if not password:
            print("⚠ Password cannot be empty")
            continue
        
        password_confirm = getpass("🔑 Confirm password: ")
        if password != password_confirm:
            print("⚠ Passwords do not match. Please try again.")
            continue
        
        break
    
    # Get output file
    default_output = input_file + '.enc'
    output_file = input(f"\n💾 Enter output file path (default: {default_output}): ").strip()
    if not output_file:
        output_file = default_output
    
    # Encrypt
    print(f"\n⏳ Encrypting file using {mode} mode...")
    encryptor = FileEncryptor()
    
    try:
        if mode == 'CBC':
            encryptor.encrypt_file_cbc(input_file, output_file, password)
        else:
            encryptor.encrypt_file_ctr(input_file, output_file, password)
        
        print(f"\n✅ SUCCESS! File encrypted successfully")
        print(f"📄 Encrypted file saved to: {output_file}")
        print(f"🔒 Encryption mode: {mode}")
        print(f"🔐 Authentication: HMAC-BLAKE2s")
        
    except Exception as e:
        print(f"\n❌ ERROR: Encryption failed")
        print(f"Details: {str(e)}")


def decrypt_file_ui():
    """User interface for file decryption"""
    print("\n" + "═" * 60)
    print(" " * 20 + "FILE DECRYPTION")
    print("═" * 60)
    
    # Get encrypted file
    input_file = get_file_path("\n📁 Enter the path of the encrypted file: ", must_exist=True)
    
    # Get password
    password = getpass("\n🔑 Enter decryption password: ")
    
    # Get output file
    default_output = input_file.replace('.enc', '_decrypted.txt') if input_file.endswith('.enc') else input_file + '_decrypted'
    output_file = input(f"\n💾 Enter output file path (default: {default_output}): ").strip()
    if not output_file:
        output_file = default_output
    
    # Decrypt
    print(f"\n⏳ Decrypting file...")
    print("⏳ Verifying HMAC tag...")
    
    encryptor = FileEncryptor()
    
    try:
        success, message = encryptor.decrypt_file(input_file, output_file, password)
        
        if success:
            print(f"\n✅ SUCCESS! {message}")
            print(f"📄 Decrypted file saved to: {output_file}")
        else:
            print(f"\n❌ FAILED: {message}")
            
    except Exception as e:
        print(f"\n❌ ERROR: Decryption failed")
        print(f"Details: {str(e)}")


def main():
    """Main application loop"""
    print_banner()
    
    encryptor = FileEncryptor()
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            encrypt_file_ui()
        elif choice == '2':
            decrypt_file_ui()
        elif choice == '3':
            print("\n👋 Thank you for using the File Encryption System!")
            print("Stay secure! 🔒\n")
            sys.exit(0)
        else:
            print("\n⚠ Invalid choice. Please enter 1, 2, or 3.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Operation cancelled by user")
        print("👋 Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
