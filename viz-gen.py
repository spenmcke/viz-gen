# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    import streamlit as st
from openai import OpenAI
import matplotlib.pyplot as plt
import io
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


# Function to call OpenAI API
def get_code_from_description(description):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Write python code using matplotlib to plot the graph: {description}",
        max_tokens=300,
        temperature=0,
    )
    return response.choices[0].text.strip()


# Streamlit app
st.title("Graph Generator from Description")

# Text input for graph description
user_description = st.text_input("Describe the graph you want:", "")

if user_description:
    if st.button("Generate Graph"):
        # Getting code from OpenAI
        generated_code = get_code_from_description(user_description)

        # Display the generated code
        st.text("Generated Code:")
        st.code(generated_code)

        # Execute the code
        exec(generated_code, globals())

        # Create a Bytes buffer to save image
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)

        # Display the image in Streamlit
        st.image(buf, caption="Generated Graph")

if __name__ == "__main__":
    run()
