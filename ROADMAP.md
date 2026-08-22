# Roadmap for Version library
1) `[MINOR]` Add a sequential convertation, using several Converters at one `.convert()` call.
1) `[MINOR]` Add a parameter to enable choosing a different convertation path, based on converters execution speed.
1) `[PATCH]` Add cache for convertors. Must support outer cache systems (f.e. Redis)
1) `[PATCH]` Add a post-execution check that `convert()` method for custom Converter class returned a Version instance, neither a None not string.
