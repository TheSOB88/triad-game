@if "%1" == "" (
    git commit -a -m "Update"
) else (
    git commit -a -m "%*"
)