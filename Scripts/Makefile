PROBLEM_NAME := Solution
CXX := clang++

# 1. Standard C++17
# 2. -O2: Optimization level 2 (Good balance for debugging)
# 3. -g: Debug symbols (REQUIRED for sanitizers to show line numbers)
# 4. -fsanitize=address,undefined: Catches out-of-bounds, overflows, leaks
# 5. -fno-omit-frame-pointer: Helps sanitizers give better stack traces
# 6. -D_LIBCPP_DEBUG=1: libc++ specific (macOS) debug mode for STL vectors/containers
# 7. Warnings: Shadow variables, conversion errors, etc.
CXXFLAGS := -std=c++17 -O2 -g \
	-fsanitize=address,undefined -fno-omit-frame-pointer \
	-D_LIBCPP_DEBUG=1 \
	-Wall -Wextra -Wshadow -Wfloat-equal \
	-Wno-unused-result -Wno-sign-conversion

$(PROBLEM_NAME): $(PROBLEM_NAME).cpp
	$(CXX) $(CXXFLAGS) $(PROBLEM_NAME).cpp -o $(PROBLEM_NAME)
# --- Fast Submit (Requires online-judge-tools) ---
# 1. python3 extracts the "url" field from problem.json
# 2. oj submit sends the file to that URL
# 3. -y flag confirms "yes" automatically
submit: $(PROBLEM_NAME)
	$(eval URL := $(shell python3 -c "import json; print(json.load(open('problem.json'))['url'])"))
	oj submit "$(URL)" $(PROBLEM_NAME).cpp -y

clean:
	rm -f $(PROBLEM_NAME) *.res *.out
	rm -rf $(PROBLEM_NAME).dSYM # Mac creates these debug folders

# --- Interactive Run (Paste yourself) ---
run: $(PROBLEM_NAME)
	./$(PROBLEM_NAME)

# --- Clipboard Run (Runs whatever you copied) ---
run_paste: $(PROBLEM_NAME)
	pbpaste | ./$(PROBLEM_NAME)

# --- Standard Test Suite ---
%.res: $(PROBLEM_NAME) %.in
	./$(PROBLEM_NAME) < $*.in > $*.res

__test_%: %.res %.out
	diff $*.res $*.out

CASES := $(sort $(basename $(wildcard *.in)))
TESTS := $(sort $(basename $(wildcard *.out)))

test: $(patsubst %,__test_%,$(TESTS))
