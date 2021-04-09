import time
import json
import gaiaclient

CLIENT = gaiaclient.Client(
    'http://localhost:1234',
    # Callback for state changes
    # machine_state_callback=print,
)

# Get state of the tester
print("State: " + CLIENT.state)


def print_with_timestamp(msg):
    from datetime import datetime
    now = datetime.now()
    now = now.strftime("%H:%M:%S")
    print(now + ": " + msg)


while True:
    # From here starts the actual test sequence

    # not audio or RF shielded and robot actions are not allowed

    # Optionally wait the test box closing
    CLIENT.wait_closing()  # <-- Optional

    print_with_timestamp("Test box closing!")

    # Wait that the test box is fully closed and ready for testing
    CLIENT.wait_ready()

    # Step 3: Test box is fully closed and we are ready for actual testing.
    print_with_timestamp("Ready for testing!")


    # Step 4: Testing is ready and we release the DUT and give test result so that test box can indicate it to operator
    CLIENT.state_triggers["ReleasePass"]()
    # The test box must be not ready after the release
    # If we don't wait here we might start the new sequence before last one is even ended
    CLIENT.wait_not_ready()
    print_with_timestamp("Test box not ready!")

    # Fake operator action. Take DUT out.
    time.sleep(2)  # <-- DO NOT USE ON PRODUCTION!
    CLIENT.applications['dut']['actions']['force-presence-off']()  # <-- DO NOT USE ON PRODUCTION!
