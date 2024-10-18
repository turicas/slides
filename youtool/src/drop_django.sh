#!/bin/bash

echo "DROP TABLE IF EXISTS dataset_empresa1;
DROP TABLE IF EXISTS dataset_empresa2;
DROP TABLE IF EXISTS dataset_empresa3;
DROP TABLE IF EXISTS dataset_empresa4;
DROP TABLE IF EXISTS auth_group CASCADE;
DROP TABLE IF EXISTS auth_group_id_seq CASCADE;
DROP TABLE IF EXISTS auth_group_permissions CASCADE;
DROP TABLE IF EXISTS auth_group_permissions_id_seq CASCADE;
DROP TABLE IF EXISTS auth_permission CASCADE;
DROP TABLE IF EXISTS auth_permission_id_seq CASCADE;
DROP TABLE IF EXISTS auth_user CASCADE;
DROP TABLE IF EXISTS auth_user_groups CASCADE;
DROP TABLE IF EXISTS auth_user_groups_id_seq CASCADE;
DROP TABLE IF EXISTS auth_user_id_seq CASCADE;
DROP TABLE IF EXISTS auth_user_user_permissions CASCADE;
DROP TABLE IF EXISTS auth_user_user_permissions_id_seq CASCADE;
DROP TABLE IF EXISTS django_admin_log CASCADE;
DROP TABLE IF EXISTS django_admin_log_id_seq CASCADE;
DROP TABLE IF EXISTS django_content_type CASCADE;
DROP TABLE IF EXISTS django_content_type_id_seq CASCADE;
DROP TABLE IF EXISTS django_migrations CASCADE;
DROP TABLE IF EXISTS django_migrations_id_seq CASCADE;
DROP TABLE IF EXISTS django_session CASCADE;" | python manage.py dbshell
python manage.py makemigrations dataset
python manage.py migrate dataset
echo "ALTER TABLE dataset_empresa1 SET (autovacuum_enabled = true);
ALTER TABLE dataset_empresa2 SET (autovacuum_enabled = true);
ALTER TABLE dataset_empresa3 SET (autovacuum_enabled = true);
ALTER TABLE dataset_empresa4 SET (autovacuum_enabled = true);" | python manage.py dbshell
for x in 1 2 3 4; do
	time python manage.py import_data copy Empresa${x} ../data/empresa_norte.csv.gz
done
