from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from grammar.HelloLexer import HelloLexer
from grammar.HelloParser import HelloParser
from grammar.HelloListener import HelloListener


class MyHelloPrinter(HelloListener):
    def enterR(self, ctx: HelloParser.RContext):
        message = ctx.ID().getText()
        print(f"Passed message: {message}")


def run_parser(text: str):
    # Standard ANTLR Pipeline
    input_stream = InputStream(text)
    lexer = HelloLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)

    # Start the parsing process at rule 'r'
    tree = parser.r()

    # Use a Walker to trigger our custom Listener
    printer = MyHelloPrinter()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

    # Print the raw tree for debugging
    print(f"Raw Tree: \n\t{tree.toStringTree(recog=parser)}")


if __name__ == "__main__":
    sample_input = "hello world"
    run_parser(sample_input)