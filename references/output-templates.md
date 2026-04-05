# Output Templates

Use these templates to keep generated practice questions consistent and token-efficient.

## Default Question Template

```markdown
## Title

## Task

## Input

## Output

## Constraints

## Sample Tests

### Sample 1

Input:
```text
...
```

Output:
```text
...
```

## Edge Cases

### Edge Case 1

Input:
```text
...
```

Output:
```text
...
```

## Marking Focus

| Test Category | Purpose | Input Characteristic | Common Mistake |
| --- | --- | --- | --- |
| Basic correctness | Verify core logic | Regular well-formed input | Solves only the happy path |
| Edge handling | Verify corner cases | Empty, repeated, or malformed-looking patterns | Ignores special cases |
| Output format | Verify exact formatting | Strict line-based output | Extra spaces or wrong ordering |

## Knowledge Points

- ...
- ...

## Hints

- ...
```

## Worked-Solution Add-On

If the user asks for a solution, append:

```markdown
## Solution Outline

- Main idea
- Key command or parsing strategy
- Why duplicates, sorting, or formatting are handled correctly

## Reference Answer

```sh
# shell or python answer here
```
```

## Multi-Question Set Template

When asked for multiple questions:

- vary the operation type
- keep difficulty progression clear
- avoid repeating the same data shape three times

Suggested sequence:

1. structured-text extraction
2. aggregation or regex
3. directory or mixed exam-style task

## Mark-My-Answer Template

When the user shares an attempted answer, respond with:

```markdown
## Quick Verdict

## What Looks Correct

- ...

## Risks

- ...

## Edge Cases To Test

| Case | Why It Matters | Expected Behavior |
| --- | --- | --- |

## Next Fix

- ...
```

## Practice Workspace Template

When the user wants a folder they can work in, create this structure on disk and then summarize it briefly in chat.

```text
testNN/
  metadata.json
  README.md
  notebook.md
  solution.sh
  data/
    sample01_input.txt
    sample02_input.txt
    sample03_input.txt
    edge01_input.txt
    edge02_input.txt
  expected/
    sample01_output.txt
    sample02_output.txt
    sample03_output.txt
    edge01_output.txt
    edge02_output.txt
  tests/
    run_tests.sh
```

For Python questions, replace `solution.sh` and `run_tests.sh` with `.py` when appropriate.

Prefer multiple visible cases by default:

- three sample cases such as `sample01` to `sample03`
- two edge cases such as `edge01` and `edge02`

Hard rule:

- do not stop at a chat-only question if the mode is `workspace`
- first create the folder and files on disk
- then fill the files
- only then summarize the result in chat

### Delegation Notes

When subagents are available:

- main agent writes `metadata.json`, `README.md`, and the placeholder solution file
- data subagent writes files under `data/` and `expected/`
- test subagent writes files under `tests/`

The main agent should then validate that the test script references the actual generated filenames.

## Mistake Summary Output Template

When the user wants to review archived mistakes, write a Markdown summary with this shape:

```markdown
# 归档错因总结

- 生成时间：
- 扫描的归档笔记数：
- 涉及主题数：

## 总览

| Topic | Notebook Count | Exercises |
| --- | --- | --- |

## 高频卡点

- ...

## 最常需要复习的命令/选项

- ...

## 最常出现的提醒

- ...

## 主题：`<topic>`

- 练习数：
- 练习列表：

### 高频卡点

- ...

### 高频错误

- ...

### 需要回顾的命令/选项

- ...

### 重要提醒

- ...

## 下一步建议

- ...
```

### README Template

```markdown
# <题目标题>

## 题目说明

## 输入

## 输出

## 要求与限制

## 文件说明

| Path | Purpose |
| --- | --- |

## 路径信息

- Windows 路径：`<windows-absolute-path>`
- WSL 路径：`<wsl-absolute-path>`

进入目录：

```sh
cd <wsl-absolute-path>
```

## 样例测试

## 边界情况

## 评分关注点

| Test Category | Purpose | Input Characteristic | Common Mistake |
| --- | --- | --- | --- |

## 考点

- ...

## 常见错误

- ...

## 如何开始

请在 `solution.sh` 中完成你的答案。

运行测试：

```sh
dash tests/run_tests.sh
```

如果你在 Windows 下练习，推荐流程：

```text
1. 在 PowerShell 中启动 WSL
2. 执行 README 里给出的 cd 命令进入当前练习目录
3. 运行：dash solution.sh < data/sample01_input.txt
4. 测试：dash tests/run_tests.sh
```
```

### Notebook Template

```markdown
# 学习笔记

## 基本信息

- 日期：
- 题目：
- 类型：
- 我这次是否独立完成：

## 我一开始的思路

- 

## 我卡住的点

- 

## 我做错的点

- 

## 需要记住的命令/选项

- `grep -E`：
- `grep -o`：
- `sed`：
- `awk`：
- `sort`：
- `uniq`：

## 这题里值得复习的例子

```sh
# 把你想记住的命令写在这里
```

## 下次再做这题时要提醒自己的话

- 
```

### Shell Test Script Template

```sh
#!/bin/dash

target="./solution.sh"
artifact_dir="./tests/.artifacts"

if [ ! -f "$target" ]; then
    echo "Missing $target"
    exit 1
fi

mkdir -p "$artifact_dir"

pass_count=0
test_count=0

print_line_count() {
    file="$1"
    awk 'END { print NR }' "$file"
}

has_trailing_newline() {
    file="$1"
    [ ! -s "$file" ] && return 0
    last_char="$(tail -c 1 "$file" 2>/dev/null)"
    [ -z "$last_char" ]
}

show_diff_excerpt() {
    expected_file="$1"
    actual_file="$2"
    diff -u "$expected_file" "$actual_file" | sed -n '1,12p'
}

compare_without_final_newline() {
    expected_file="$1"
    actual_file="$2"
    expected_tmp="$(mktemp)"
    actual_tmp="$(mktemp)"

    awk '{ print }' "$expected_file" > "$expected_tmp"
    awk '{ print }' "$actual_file" > "$actual_tmp"

    if cmp -s "$expected_tmp" "$actual_tmp"; then
        result=0
    else
        result=1
    fi

    rm -f "$expected_tmp" "$actual_tmp"
    return "$result"
}

run_case() {
    name="$1"
    input_file="$2"
    expected_file="$3"
    reason="$4"

    test_count=$((test_count + 1))
    actual_file="$artifact_dir/$name.actual.txt"
    rm -f "$actual_file"

    if ! dash "$target" < "$input_file" > "$actual_file"; then
        echo "FAIL: $name"
        echo "Reason: command exited with non-zero status"
        echo "Actual output path: $actual_file"
        return
    fi

    if diff -u "$expected_file" "$actual_file"; then
        echo "PASS: $name"
        pass_count=$((pass_count + 1))
        rm -f "$actual_file"
    else
        echo "FAIL: $name"
        expected_lines="$(print_line_count "$expected_file")"
        actual_lines="$(print_line_count "$actual_file")"

        if compare_without_final_newline "$expected_file" "$actual_file"; then
            echo "Reason: content matches but trailing newline handling is different"
        elif [ "$expected_lines" != "$actual_lines" ]; then
            echo "Reason: line count differs"
            echo "Expected lines: $expected_lines"
            echo "Actual lines:   $actual_lines"
        else
            echo "Reason: $reason"
        fi

        if has_trailing_newline "$expected_file" && ! has_trailing_newline "$actual_file"; then
            echo "Hint: expected output ends with a newline, but your output does not"
        elif ! has_trailing_newline "$expected_file" && has_trailing_newline "$actual_file"; then
            echo "Hint: your output ends with an extra trailing newline"
        fi

        echo "Expected output path: $expected_file"
        echo "Actual output path:   $actual_file"
        echo "Diff excerpt:"
        show_diff_excerpt "$expected_file" "$actual_file"
    fi
}

run_case_group() {
    prefix="$1"
    reason="$2"

    for input_file in data/${prefix}[0-9][0-9]_input.txt; do
        [ -f "$input_file" ] || continue
        file_name="${input_file##*/}"
        case_name="${file_name%_input.txt}"
        expected_file="expected/${case_name}_output.txt"
        run_case "$case_name" "$input_file" "$expected_file" "$reason"
    done
}

run_case_group "sample" "output mismatch on a visible sample case"
run_case_group "edge" "edge-case handling is incorrect"

echo "$pass_count/$test_count tests passed"
```

### Shell Placeholder Template

```sh
#!/bin/dash
# 在 Windows 上可以这样运行：
# 1. 在 PowerShell 中启动 WSL
# 2. cd 到这个练习目录
# 3. 执行：dash solution.sh < data/sample01_input.txt
# 4. 测试：dash tests/run_tests.sh
#
# 在下面写你的答案。
```
