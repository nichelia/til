# Discover big files

## Description

The challenge of finding big files through the terminal. Ideally I want to be able to see what files are consuming how much in a directory so I can do a manual nuke!

## Resolution

* Open terminal and use the below

```bash
alias big='du -ah . | sort -rh | head -20'
alias big-files='ls -1Rhs | sed -e "s/^ *//" | grep "^[0-9]" | sort -hr | head -n20'
```