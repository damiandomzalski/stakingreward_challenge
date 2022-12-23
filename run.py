import csv

def incFrom(n):
  return n + 1

def text(n):
  return str(n)

def concat(str1, str2):
  return str1 + str2

def split(string, delimiter):
  return string.split(delimiter)

def spread(arr):
  return [float(x) for x in arr]

def sum(arr):
  return sum(arr)

def bte(bool1, bool2):
  return bool1 == bool2

def eval_formula(formula, data, row, col, col_label_map):
  stack = []
  result = 0
  for token in formula:
    if token.isdigit():
      stack.append(int(token))
    elif token[0].isalpha():
      if token[0] in col_label_map:
        col_label = token[0]
        if len(token) > 1:
          if token[1] == "^":
            prev_row_index = row - 1
            while prev_row_index >= 0:
              if data[prev_row_index][col_label_map[col_label]] and data[prev_row_index][col_label_map[col_label]][0] == "=":
                stack.append(eval_formula(data[prev_row_index][col_label_map[col_label]][1:], data, prev_row_index, col_label_map[col_label], col_label_map))
                break
              elif data[prev_row_index][col_label_map[col_label]]:
                stack.append(float(data[prev_row_index][col_label_map[col_label]]))
                break
              prev_row_index -= 1
          elif token[1] == "^v":
            prev_col_index = col - 1
            while prev_col_index >= 0:
              if data[row][prev_col_index] and data[row][prev_col_index][0] == "=":
                stack.append(eval_formula(data[row][prev_col_index][1:], data, row, prev_col_index, col_label_map))
                break
              elif data[row][prev_col_index]:
                stack.append(float(data[row][prev_col_index]))
                break
              prev_col_index -= 1
          elif token[1:].isdigit():
            stack.append(float(data[int(token[1:])][col_label_map[col_label]]))
          else:
            stack.append(float(data[row][col_label_map[col_label]]))
      elif token[0] == "@":
        label = token[1:].split(" ")[0]
        row_index = int(token[1:].split(" ")[1])
        stack.append(float(data[row_index][col_label]))
      elif token == "^^":
        prev_row_index = row - 1
        while prev_row_index >= 0:
            if data[prev_row_index][col] and data[prev_row_index][col][0] == "=":
                stack.append(eval_formula(data[prev_row_index][col][1:], data, prev_row_index, col, col_label_map))
                break
            elif data[prev_row_index][col]:
                stack.append(float(data[prev_row_index][col]))
                break
            prev_row_index -= 1

def run_formulas(csv_file):
    data = []
    col_label_map = {}
    with open(csv_file, "r") as file:
        reader = csv.reader(file, delimiter="|")
        row_index = 0
        for row in reader:
            data.append([])
            col_index = 0
            for col in row:
                if not col or not col[0]:
                    continue
                if row_index == 0:
                    col_label_map[col[1:]] = col_index
                elif col[0] == "=":
                    data[row_index].append(eval_formula(col[1:], data, row_index, col_index, col_label_map))
                else:
                    data[row_index].append(col)
                col_index += 1
            row_index += 1
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerows(data)
    return data

run_formulas("dataset.csv")