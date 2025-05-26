
import argparse
import pandas as pd
from openai import OpenAI


API_KEY = " "  # Replace 'API_KEY' with your own key
client = OpenAI(api_key=API_KEY)


# Prompt template
PROMPT_TEMPLATE = """
Definition：
Scenario-aware Functional Equivalent (SaFE) API pair refers to APIs that, regardless of whether their original functionalities are identical, can be employed interchangeably within the same application scenarios to achieve equivalent functionality.

Task Description:
The following content is derived from a SO post concerning the selection and application of  SaFE APIs. It includes the post title, question description, and corresponding answers, which may contain code snippets, references to API documentation, and discussions of specific programming functions or APIs.

Your task is twofold:
1. Analyze the provided content to identify potential SaFE API pairs based on their functional equivalence and usage context.
2. Generate systematic performance evaluation cases to assess and compare the performance (e.g., execution time, memory usage) of the identified SaFE API pairs.

Requirements:
1. Potential SaFE API Extraction
Analyze the given text and code snippets, and extract all referenced APIs or functions, clearly providing the complete API name prefixed by its package (e.g., tensorflow.keras.Model.fit). 
Identify pairs of APIs that exhibit functional equivalence under specific usage scenarios; label them clearly as api1 and api2.

2. Performance Evaluation Case Generation
Once potential SaFE APIs are detected, systematically generate complete Python-based performance evaluation cases with the following criteria:
Prepare input data of four different scales: approximately 10, 100, 1,000, and 10,000 elements or records.
For each scale, generate random yet representative evaluation data suitable in shape, data type, or structure to the APIs under evaluation.

A post demo example：
Title :  Efficient row elements multiplication in numpy
Question :  Is there any efficient way to find the multiplication of every row in a matrix using numpy？
Anwser1 :   np.prod is what you're looking for. a = np.array([[1, 2], [3, 4]]) print(np.prod(a, axis=1)) # Prints array([2, 12]) 
Anwser2 :   ……
After analysis of the above SO post content, the SaFE API pair can be numpy.prod and numpy.multiply.reduce
api1 = "numpy.prod"
api2 = "numpy.multiply.reduce"
test_sizes = [10, 100, 1000, 10000]
N = test_sizes[0]
A = np.random.rand(N, 2).astype(np.float32)
# Method 1: Using numpy.prod
def method_v1(A):
    return np.prod(A, axis=1)
# Method 2: Using numpy.multiply.reduce
def method_v2(A):
    return np.multiply.reduce(A, axis=1)
"""

def main():
    parser = argparse.ArgumentParser(
        description="Read an Excel of SO answers and generate performance case via GPT."
    )
    parser.add_argument('input_file', help='Excel file with "answers_text" and "code_blocks" columns')
    parser.add_argument('--output', default='generated_output.xlsx',
                        help='Filename for the output Excel (default: generated_output.xlsx)')
    args = parser.parse_args()

    df = pd.read_excel(args.input_file)
    df["generated_code"] = None
    total = len(df)

    for idx, row in df.iterrows():
        # Safely coerce NaN or non-string to empty string
        raw_text = row.get("answers_text")
        text_part = raw_text if isinstance(raw_text, str) else ""

        raw_code = row.get("code_blocks")
        code_part = raw_code if isinstance(raw_code, str) else ""

        combined = (
            "### Answer Text ###\n" +
            text_part +
            "\n\n### Code Snippets ###\n" +
            code_part
        )

        messages = [
            {"role": "system", "content": "You are a professional AI assistant, adept at analyzing text and code and generating test cases."},
            {"role": "user", "content": combined},
            {"role": "user", "content": PROMPT_TEMPLATE}
        ]

        try:
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.0,
                max_tokens=2000
            )
            df.at[idx, "generated_code"] = resp.choices[0].message.content
            print(f"[{idx+1}/{total}] Generated successfully.")
        except Exception as e:
            print(f"[{idx+1}/{total}] Error: {e}")
            df.at[idx, "generated_code"] = f"Error: {e}"

    df.to_excel(args.output, index=False)
    print(f"Done! Results saved to {args.output}")


if __name__ == "__main__":
    main()