CREATE TABLE IF NOT EXISTS python_package_version
(
    id                         serial       NOT NULL
        CONSTRAINT python_package_version_pkey
            PRIMARY KEY,
    package_name               varchar(256) NOT NULL,
    package_version            varchar(256),
    os_name                    varchar(256) NOT NULL,
    os_version                 varchar(256) NOT NULL,
    python_version             varchar(256) NOT NULL,
    entity_id                  integer      NOT NULL
        CONSTRAINT python_package_version_entity_id_fkey
            REFERENCES python_package_version_entity
            ON DELETE CASCADE,
    python_package_index_id    integer
        CONSTRAINT python_package_version_python_package_index_id_fkey
            REFERENCES python_package_index
            ON DELETE CASCADE,
    python_package_metadata_id integer
        CONSTRAINT python_package_version_python_package_metadata_id_fkey
            REFERENCES python_package_metadata
            ON DELETE CASCADE,
    CONSTRAINT python_package_version_package_name_package_version_python__key
        UNIQUE (package_name, package_version, python_package_index_id, os_name, os_version, python_version)
);

ALTER TABLE python_package_version
    OWNER TO postgres;

CREATE INDEX IF NOT EXISTS python_package_version_index_idx_00
    ON python_package_version (package_name, package_version);

CREATE INDEX IF NOT EXISTS python_package_version_index_idx_10
    ON python_package_version (package_name, package_version, os_name);

CREATE INDEX IF NOT EXISTS python_package_version_index_idx_11
    ON python_package_version (package_name, package_version, os_version);

CREATE INDEX IF NOT EXISTS python_package_version_index_idx_12
    ON python_package_version (package_name, package_version, python_version);

CREATE INDEX IF NOT EXISTS python_package_version_index_idx_20
    ON python_package_version (package_name, package_version, os_name, os_version);

CREATE INDEX IF NOT EXISTS python_package_version_index_idx_21
    ON python_package_version (package_name, package_version, os_name, python_version);

CREATE INDEX IF NOT EXISTS python_package_version_index_idx_22
    ON python_package_version (package_name, package_version, os_version, python_version);

CREATE INDEX IF NOT EXISTS python_package_version_index_idx_30
    ON python_package_version (package_name, package_version, os_name, os_version, python_version);

INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (1, 'absl-py', '0.7.1', 'rhel', '8', '3.6', 1, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (2, 'astor', '0.8.0', 'rhel', '8', '3.6', 2, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (3, 'gast', '0.2.2', 'rhel', '8', '3.6', 3, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (4, 'grpcio', '1.22.0', 'rhel', '8', '3.6', 4, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (5, 'h5py', '2.9.0', 'rhel', '8', '3.6', 5, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (6, 'keras-applications', '1.0.8', 'rhel', '8', '3.6', 6, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (7, 'keras-preprocessing', '1.1.0', 'rhel', '8', '3.6', 7, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (8, 'markdown', '3.1.1', 'rhel', '8', '3.6', 8, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (9, 'mock', '3.0.5', 'rhel', '8', '3.6', 9, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (10, 'numpy', '1.16.4', 'rhel', '8', '3.6', 10, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (11, 'protobuf', '3.9.0', 'rhel', '8', '3.6', 11, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (12, 'six', '1.12.0', 'rhel', '8', '3.6', 12, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (13, 'tensorboard', '1.13.1', 'rhel', '8', '3.6', 13, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (14, 'tensorflow', '1.13.1', 'rhel', '8', '3.6', 14, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (15, 'tensorflow-estimator', '1.13.0', 'rhel', '8', '3.6', 15, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (16, 'termcolor', '1.1.0', 'rhel', '8', '3.6', 16, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (17, 'werkzeug', '0.15.5', 'rhel', '8', '3.6', 17, 1, null);
INSERT INTO python_package_version (id, package_name, package_version, os_name, os_version, python_version, entity_id, python_package_index_id, python_package_metadata_id) VALUES (18, 'wheel', '0.33.4', 'rhel', '8', '3.6', 18, 1, null);
