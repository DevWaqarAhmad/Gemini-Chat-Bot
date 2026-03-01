"""
Butt Karahi - backend.py Direct Test Script
============================================
Directly imports backend.py — No Flask server needed!
Run: python test_backend.py
Or interactive: python test_backend.py chat
"""

import sys
import time

# ==============================
# ANSI Colors
# ==============================
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# ==============================
# Import Backend
# ==============================
print(f"{YELLOW}[*] Importing backend.py ...{RESET}")
try:
    import backend
    print(f"{GREEN}[✓] backend.py imported successfully!{RESET}\n")
except ImportError as e:
    print(f"{RED}[✗] Could not import backend.py: {e}{RESET}")
    print(f"{YELLOW}    → Make sure test_backend.py is in same folder as backend.py{RESET}")
    sys.exit(1)
except Exception as e:
    print(f"{RED}[✗] Error loading backend.py: {e}{RESET}")
    sys.exit(1)

# ==============================
# Test Cases
# ==============================
TEST_CASES = [
    # ── English ──────────────────────────────────────────────────
    {
        "category": "Identity",
        "message": "Who are you?",
        "expect_keywords": ["butt karahi", "ai", "agent", "help"]
    },
    {
        "category": "Location",
        "message": "Where are your restaurant locations?",
        "expect_keywords": ["mississauga", "pickering", "canada"]
    },
    {
        "category": "Featured Menu",
        "message": "What are your featured dishes?",
        "expect_keywords": ["karahi", "chicken", "goat", "veal"]
    },
    {
        "category": "Kids Menu",
        "message": "Do you have a kids menu?",
        "expect_keywords": ["fries", "roll", "kids"]
    },
    {
        "category": "Pricing",
        "message": "What are the prices?",
        "expect_keywords": ["cad", "$", "price"]
    },
    {
        "category": "Greeting",
        "message": "Hello!",
        "expect_keywords": ["hello", "hi", "help", "assist"]
    },
    {
        "category": "Introduction",
        "message": "Tell me about Butt Karahi",
        "expect_keywords": ["butt karahi", "halal", "pakistani", "food", "fresh"]
    },
    {
        "category": "Opening Hours",
        "message": "What are your opening hours?",
        "expect_keywords": []  # Just check response exists
    },
    {
        "category": "Contact",
        "message": "How can I contact you?",
        "expect_keywords": []
    },

    # ── Urdu ──────────────────────────────────────────────────────
    {
        "category": "Urdu - Location",
        "message": "آپ کے ریسٹورنٹ کہاں ہیں؟",
        "expect_keywords": []
    },
    {
        "category": "Urdu - Menu",
        "message": "مینو بتائیں",
        "expect_keywords": []
    },

    # ── Hindi ─────────────────────────────────────────────────────
    {
        "category": "Hindi - Menu",
        "message": "मेनू क्या है?",
        "expect_keywords": []
    },

    # ── Edge Cases ────────────────────────────────────────────────
    {
        "category": "Edge - Off-topic",
        "message": "Can you help me with Python programming?",
        "expect_keywords": []
    },
    {
        "category": "Edge - Emoji",
        "message": "What's your best dish? 🍛🔥",
        "expect_keywords": []
    },
    {
        "category": "Edge - Empty spaces",
        "message": "   ",
        "expect_keywords": []  # Should handle gracefully
    },
]

# ==============================
# Helpers
# ==============================
def check_keywords(text: str, keywords: list) -> bool:
    if not keywords:
        return True
    return any(kw.lower() in text.lower() for kw in keywords)


def print_header():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  Butt Karahi - backend.py Test Suite{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")


# ==============================
# Check Training Data Loaded
# ==============================
def check_training_data():
    print(f"{YELLOW}[*] Checking training data (data.txt) ...{RESET}")
    count = len(backend.TRAINING_DATA)
    if count == 0:
        print(f"{YELLOW}[⚠] data.txt is empty or not found! Responses may be generic.{RESET}\n")
    else:
        pairs = count // 2
        print(f"{GREEN}[✓] {pairs} Q&A pairs loaded from data.txt{RESET}\n")


# ==============================
# Run All Tests
# ==============================
def run_tests():
    print_header()
    check_training_data()

    passed = 0
    failed = 0
    errors = 0
    failed_list = []

    for i, test in enumerate(TEST_CASES, 1):
        print(f"{CYAN}[{i:02d}/{len(TEST_CASES)}] {test['category']}{RESET}")
        print(f"       Q: {test['message']}")

        # Skip whitespace-only inputs gracefully
        if not test["message"].strip():
            print(f"       {YELLOW}[⚠ SKIPPED] Whitespace input — testing graceful handling{RESET}")
            try:
                response = backend.generate_response(test["message"])
                print(f"       A: {str(response)[:100]}")
                print(f"       {GREEN}[✓ No crash]{RESET}\n")
                passed += 1
            except Exception as e:
                print(f"       {RED}[✗] Crashed on empty input: {e}{RESET}\n")
                errors += 1
            continue

        try:
            start = time.time()
            response = backend.generate_response(test["message"])
            elapsed = time.time() - start

            if not response or not response.strip():
                print(f"       {RED}[✗] Empty response!{RESET}\n")
                failed += 1
                failed_list.append((test["category"], "Empty response"))
                continue

            # Show preview
            preview = response[:150].replace("\n", " ")
            print(f"       A: {preview}{'...' if len(response) > 150 else ''}")
            print(f"       ⏱  {elapsed:.2f}s", end="  ")

            if check_keywords(response, test["expect_keywords"]):
                print(f"{GREEN}[✓ PASS]{RESET}\n")
                passed += 1
            else:
                print(f"{YELLOW}[⚠ KEYWORD MISS] Expected one of: {test['expect_keywords']}{RESET}\n")
                failed += 1
                failed_list.append((test["category"], f"Expected: {test['expect_keywords']}"))

        except Exception as e:
            print(f"       {RED}[✗] EXCEPTION: {e}{RESET}\n")
            errors += 1
            failed_list.append((test["category"], str(e)))

        time.sleep(0.3)  # Small delay between API calls

    # ── Summary ───────────────────────────────────────────────────
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  TEST SUMMARY{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")
    print(f"  Total   : {len(TEST_CASES)}")
    print(f"  {GREEN}Passed  : {passed}{RESET}")
    print(f"  {YELLOW}Failed  : {failed}{RESET}")
    print(f"  {RED}Errors  : {errors}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    if failed_list:
        print(f"{YELLOW}Issues Found:{RESET}")
        for name, detail in failed_list:
            print(f"  • {name} → {detail}")
        print()

    return passed, failed, errors


# ==============================
# Interactive Chat Mode
# ==============================
def interactive_mode():
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  Interactive Chat  (type 'quit' to exit){RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")

    check_training_data()

    while True:
        try:
            user_input = input(f"{CYAN}You: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break

        if user_input.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        if not user_input:
            continue

        try:
            start = time.time()
            response = backend.generate_response(user_input)
            elapsed = time.time() - start
            print(f"{GREEN}Bot:{RESET} {response}")
            print(f"{YELLOW}     ⏱ {elapsed:.2f}s{RESET}\n")
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}\n")


# ==============================
# Entry Point
# ==============================
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"

    if mode == "chat":
        # python test_backend.py chat
        interactive_mode()
    else:
        # python test_backend.py
        passed, failed, errors = run_tests()

        if errors == 0:
            try:
                print("Interactive chat mode mein jaana chahte ho? (y/n): ", end="")
                choice = input().strip().lower()
                if choice == "y":
                    interactive_mode()
            except (KeyboardInterrupt, EOFError):
                pass