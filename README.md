# project-code

This language is designed to test whether your poems match rhyme schemes you provide. 

## Running the program

In order to run the program, you must have the poem you want to run stored in the same folder as `interpreter.py`. Three sample poems, "simple.txt", "sonnet.txt", and "presentation.txt", are provided.

From there, you initialize an interpreter, with no additional parameters. For the purposes of this readme, we call our interpreter "demo".

```
demo = Interpreter
```

There are then three commands that a user can run.

### Check a pattern passed in on the command line

To check if "simple.txt" is of the rhyme scheme "aaba", we can call:
```
demo.checkPattern("simple.txt", "aaba")
```
The program will then output whether or not the poem matches the scheme, or if the scheme is even valid.

### Add a rhyme scheme

To add a rhyme scheme, use the `addForm` command.
```
demo.addForm("aaba", "simpleForm")
```

You can also use parentheses to speficy repeated segments. Segments in between parentheses can appear in the poem 0 or more times. Thus, `aaba` can also be represented as `(a)ba`.

### Check a scheme already stored in the interpreter. 

To use a scheme already stored in the interpreter, we use the `checkForm` command.

```
demo.cehckForm("simple.txt", "simpleForm")
```

The interpreter will find that form in its dictionary, and then call `checkPattern` using that form.

### Interaction with the user is handled through error messages, which should be descriptive of why your poem does or doesn't match a scheme, or why you scheme is invalid!