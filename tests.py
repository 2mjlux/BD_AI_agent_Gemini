#from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from config import MAX_CHARS

#print("Result for current directory:")
#print(get_files_info("calculator", "."))
#print()
#print("Result for 'pkg' directory:")
#print(get_files_info("calculator", "pkg"))
#print()
#print("Result for '/bin' directory:")
#print(get_files_info("calculator", "/bin"))
#print()
#print("Result for '../' directory:")
#print(get_files_info("calculator", "../"))
#print()


# Test 1: Lorem ipsum truncation test
print("\n1. Testing lorem.txt (should truncate at 10000 chars):")
result = get_file_content("calculator", "lorem.txt")
print(f"Length: {len(result)} chars")
if "[...File" in result and "truncated" in result:
    print("Truncation message found")

# Test 2: Read main.py
print("\n2. Testing calculator/main.py:")
result = get_file_content("calculator", "main.py")
print(result)

# Test 3: Read pkg/calculator.py
print("\n3. Testing calculator/pkg/calculator.py:")
result = get_file_content("calculator", "pkg/calculator.py")
print(result)

# Test 4: Try to read outside working directory
print("\n4. Testing /bin/cat (should fail - outside directory):")
result = get_file_content("calculator", "/bin/cat")
print(result)

# Test 5: Try to read non-existent file
print("\n5. Testing pkg/does_not_exist.py (should fail - file not found):")
result = get_file_content("calculator", "pkg/does_not_exist.py")
print(result)
