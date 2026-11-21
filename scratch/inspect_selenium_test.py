with open('scratch/test_browser_selenium.py', 'r', encoding='utf-8') as f:
    code = f.read()

print("Selenium test length:", len(code))
print("First 30 lines:\n", '\n'.join(code.splitlines()[:30]))
