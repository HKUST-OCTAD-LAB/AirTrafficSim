Files under here are part of the rewrite to make it more modular. They are licensed under the more permissive [MIT license](./LICENSE).

Once stabilised, the code will be moved to the main directory.

# Goals

- prefer pure functions over deep inheritance hierarchies
- array first: any object that conforms to the [Array API](https://data-apis.org/array-api/) should be usable (e.g. NumPy, JAX, PyTorch, CuPy)
- support for automatic differentiation via JAX