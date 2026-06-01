from langchain_classic.output_parsers.structured import StructuredOutputParser, ResponseSchema

schema = [
    ResponseSchema(name='errors', description='list of error messages found in the log file'),
    ResponseSchema(name='warnings', description='list of warning messages found in the log file'),
    ResponseSchema(name='summary', description='a concise summary of the log file based on the user query'),
]

parser = StructuredOutputParser.from_response_schemas(schema)

