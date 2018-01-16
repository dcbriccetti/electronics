import time
import mcp3008

while True:
    with mcp3008.MCP3008() as adc:
        print(adc.read_all())
        print(adc.read([mcp3008.CH0])[0])
    time.sleep(2)
    