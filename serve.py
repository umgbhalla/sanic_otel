from sanic import Sanic
from sanic import response
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)


app = Sanic("potato")

ctx = trace.get_current_span().get_span_context()

link_from_current = trace.Link(ctx)

# webapp path defined used route decorator
@app.route("/")
def run(request):
    with tracer.start_as_current_span("span-name") as span:
        # do some work that 'span' will track
        current_span = trace.get_current_span()
        current_span.add_event("new event like a post event ?")
        print(current_span)
        # When the 'with' block goes out of scope, 'span' is closed for you
    return response.text("Hello World !")


# debug logs enabled with debug = True
app.run(host ="0.0.0.0", port = 8080, debug = True)

