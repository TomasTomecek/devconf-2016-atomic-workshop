#!/usr/bin/python3
import os
import signal

# signal id -> signal name
SIGNALS_TO_NAMES_DICT = dict((getattr(signal, n), n) \
    for n in dir(signal) if n.startswith('SIG') and '_' not in n )

print("My PID is %d, you can stop me with SIGINT1" % os.getpid())

while True:
    info = signal.sigwaitinfo(range(1, signal.NSIG))

    if info.si_signo == signal.SIGUSR1:
        print("Received deadly signal %r" % (SIGNALS_TO_NAMES_DICT[info.si_signo]))
        break
    else:
        print("Received signal %r" % (SIGNALS_TO_NAMES_DICT[info.si_signo]))

