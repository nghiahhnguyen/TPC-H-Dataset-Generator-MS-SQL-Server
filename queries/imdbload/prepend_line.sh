for sql in ./*.sql; do
    sed -i '1i\set showplan_all on;\nGO\n' "$sql"
done
