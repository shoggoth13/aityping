# AITyping

Using AI to "type" (really validate) Python code. Tries to be "Ambient AI".
Allows you to do things like:

```python
isinstance("Julia", PersonName)
>>> True

isinstance("Idaho", PersonName)
>>> False
```

## 🚀 Overview

The `typing` module in Python helps the user understand the codebase better.
They are useful for distinguishing between ints and strings, for example.
The `aityping` module helps do "fuzzy typing".
This is really run-time validation. 
However, it's bundled up as a type so that you can use it with Pydantic Models easily.

## 📄 Installation
`pip install aityping`

## 💻 Usage

### Setup

First, you need to set your OpenAI key:

```python
import os
os.environ["OPENAI_API_KEY"] = 'YOUR_OPENAI_API_KEY'
```

### Quickstart

Next we import the `get_ai_type` function:

```python
from aityping import get_ai_type
```

After that is done we can create a "type" with some fuzzy logic
```python
PersonName = get_ai_type("is a persons name")
```

We can now use this to do type checking as we would with any other type.

```python
isinstance("Julia", PersonName)
>>> True

isinstance("Idaho", PersonName)
>>> False
```

We can also use it to type a Pydantic model and then have that do validation.
```python
from pydantic import BaseModel

class Record(BaseModel):
    name: PersonName

Record(name='Julia')
>>> Record(name='Julia')

Record(name='Idaho')
>>> ValidationError: 1 validation error for Record
>>> name
>>>   Flagged as invalid. (type=type_error)
```

### LLM Configuration

By default, this will use the following LLM configuration:

```python
ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
```

If you want to use a different configuration, you easily can!

```python
from langchain.chat_models import ChatOpenAI
PersonName = get_ai_type("is a persons name", llm=ChatOpenAI(model="gpt-4"))
```

