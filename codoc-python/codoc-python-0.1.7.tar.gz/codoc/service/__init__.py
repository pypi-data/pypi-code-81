"""
The service layer is created to expose pure functionality of the framework.

We try to develop things in a pure functional fashion without side effects, and
general adhere to immutable data types.

We utilize a service layer with the intent of separating
the domain model from usage.

The top level of the service layer should expose a bunch of functions
that can  be used by a given entry point
(be it the CLI or when used as a functional framework)

Our usage of a service layer is heavily inspired by
 [Architectural Patterns In Python](https://cosmicpython.com).

For more info about the interface of the function, please go to the examples

"""
