import sys
from poller import Poller

print(sys.argv[1])
print(Poller.poll_base(sys.argv[1], 'tFXe9N6jd'))
