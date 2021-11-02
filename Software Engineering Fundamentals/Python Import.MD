```
import foo
print(foo.bar('hi')) # 1

import foo as fooFile
print(fooFile.bar('hi')) # 2

from foo import bar
print(bar('hi')) # 3

from foo import *
print(bar('hi')) # 4
```

#1 This is fine, and is useful when using many functions from an import

#2 This is like (#1), except useful when the name of the import is quite generic and could be confused with something else

#3 This is often useful when you only need to import very particular functions from a file

#4 This is not recommended, this imports a whole number of functions that could conflict with other names in the namespace
