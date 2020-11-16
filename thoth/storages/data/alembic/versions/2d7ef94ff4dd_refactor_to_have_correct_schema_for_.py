"""Refactor to have correct Schema for Python Software Stack

Revision ID: 2d7ef94ff4dd
Revises: 1a8150ac45e0
Create Date: 2020-10-09 16:04:29.846495+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2d7ef94ff4dd'
down_revision = '1a8150ac45e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('external_python_requirements',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('requirements_hash', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('external_python_requirements_lock',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('requirements_lock_hash', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('python_requirements',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('requirements_hash', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('python_requirements_lock',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('requirements_lock_hash', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('external_python_software_stack',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('external_python_requirements_id', sa.Integer(), nullable=True),
    sa.Column('external_python_requirements_lock_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['external_python_requirements_id'], ['external_python_requirements.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['external_python_requirements_lock_id'], ['external_python_requirements_lock.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('python_software_stack',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('software_stack_type', postgresql.ENUM('INSPECTION', 'ADVISED', name='software_stack_type', create_type=False), nullable=True),
    sa.Column('performance_score', sa.Float(), nullable=True),
    sa.Column('overall_score', sa.Float(), nullable=True),
    sa.Column('python_requirements_id', sa.Integer(), nullable=True),
    sa.Column('python_requirements_lock_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['python_requirements_id'], ['python_requirements.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['python_requirements_lock_id'], ['python_requirements_lock.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('adviser_run',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('adviser_document_id', sa.Text(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('adviser_version', sa.Text(), nullable=False),
    sa.Column('adviser_name', sa.Text(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('limit', sa.Integer(), nullable=True),
    sa.Column('origin', sa.Text(), nullable=True),
    sa.Column('source_type', postgresql.ENUM('CLI', 'KEBECHET', 'S2I', 'GITHUB_APP', 'JUPYTER_NOTEBOOK', name='source_type', create_type=False), nullable=True),
    sa.Column('is_s2i', sa.Boolean(), nullable=True),
    sa.Column('debug', sa.Boolean(), nullable=False),
    sa.Column('need_re_run', sa.Boolean(), nullable=True),
    sa.Column('re_run_adviser_id', sa.Text(), nullable=True),
    sa.Column('limit_latest_versions', sa.Integer(), nullable=True),
    sa.Column('adviser_error', sa.Boolean(), nullable=False),
    sa.Column('recommendation_type', postgresql.ENUM('STABLE', 'TESTING', 'LATEST', name='recommendation_type', create_type=False), nullable=False),
    sa.Column('requirements_format', postgresql.ENUM('PIPENV', name='requirements_format', create_type=False), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('advised_configuration_changes', sa.Boolean(), nullable=False),
    sa.Column('additional_stack_info', sa.Boolean(), nullable=False),
    sa.Column('user_software_stack_id', sa.Integer(), nullable=True),
    sa.Column('external_run_software_environment_id', sa.Integer(), nullable=True),
    sa.Column('external_build_software_environment_id', sa.Integer(), nullable=True),
    sa.Column('external_hardware_information_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['external_build_software_environment_id'], ['external_software_environment.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['external_hardware_information_id'], ['external_hardware_information.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['external_run_software_environment_id'], ['external_software_environment.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_software_stack_id'], ['external_python_software_stack.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('has_external_python_requirement',
    sa.Column('external_python_requirements_id', sa.Integer(), nullable=False),
    sa.Column('python_package_requirement_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['external_python_requirements_id'], ['external_python_requirements.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['python_package_requirement_id'], ['python_package_requirement.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('external_python_requirements_id', 'python_package_requirement_id')
    )
    op.create_table('has_external_python_requirement_lock',
    sa.Column('external_python_requirements_locked_id', sa.Integer(), nullable=False),
    sa.Column('python_package_version_entity_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['external_python_requirements_locked_id'], ['external_python_requirements_lock.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['python_package_version_entity_id'], ['python_package_version_entity.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('external_python_requirements_locked_id', 'python_package_version_entity_id')
    )
    op.create_table('has_python_requirements',
    sa.Column('python_requirements_id', sa.Integer(), nullable=False),
    sa.Column('python_package_requirement_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['python_package_requirement_id'], ['python_package_requirement.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['python_requirements_id'], ['python_requirements.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('python_requirements_id', 'python_package_requirement_id')
    )
    op.create_table('inspection_run',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('inspection_document_id', sa.Text(), nullable=False),
    sa.Column('inspection_result_number', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('amun_version', sa.Text(), nullable=True),
    sa.Column('build_requests_cpu', sa.Float(), nullable=True),
    sa.Column('build_requests_memory', sa.Float(), nullable=True),
    sa.Column('run_requests_cpu', sa.Float(), nullable=True),
    sa.Column('run_requests_memory', sa.Float(), nullable=True),
    sa.Column('inspection_sync_state', postgresql.ENUM('PENDING', 'SYNCED', name='inspection_sync_state', create_type=False), nullable=False),
    sa.Column('build_hardware_information_id', sa.Integer(), nullable=True),
    sa.Column('run_hardware_information_id', sa.Integer(), nullable=True),
    sa.Column('build_software_environment_id', sa.Integer(), nullable=True),
    sa.Column('run_software_environment_id', sa.Integer(), nullable=True),
    sa.Column('dependency_monkey_run_id', sa.Integer(), nullable=True),
    sa.Column('inspection_software_stack_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['build_hardware_information_id'], ['hardware_information.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['build_software_environment_id'], ['software_environment.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['dependency_monkey_run_id'], ['dependency_monkey_run.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['inspection_software_stack_id'], ['python_software_stack.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['run_hardware_information_id'], ['hardware_information.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['run_software_environment_id'], ['software_environment.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('provenance_checker_run',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('provenance_checker_document_id', sa.Text(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('provenance_checker_version', sa.Text(), nullable=False),
    sa.Column('provenance_checker_name', sa.Text(), nullable=False),
    sa.Column('origin', sa.Text(), nullable=True),
    sa.Column('debug', sa.Boolean(), nullable=False),
    sa.Column('provenance_checker_error', sa.Boolean(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('user_software_stack_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_software_stack_id'], ['external_python_software_stack.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'user_software_stack_id')
    )
    op.create_table('advised',
    sa.Column('adviser_run_id', sa.Integer(), nullable=False),
    sa.Column('python_software_stack_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['adviser_run_id'], ['adviser_run.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['python_software_stack_id'], ['python_software_stack.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('adviser_run_id', 'python_software_stack_id')
    )
    op.create_table('has_python_requirement_lock',
    sa.Column('python_requirements_lock_id', sa.Integer(), nullable=False),
    sa.Column('python_package_version_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['python_package_version_id'], ['python_package_version.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['python_requirements_lock_id'], ['python_requirements_lock.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('python_requirements_lock_id', 'python_package_version_id')
    )
    op.create_table('has_unresolved',
    sa.Column('adviser_run_id', sa.Integer(), nullable=False),
    sa.Column('python_package_version_entity_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['adviser_run_id'], ['adviser_run.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['python_package_version_entity_id'], ['python_package_version_entity.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('adviser_run_id', 'python_package_version_entity_id')
    )
    op.create_table('pi_conv1d',
    sa.Column('component', sa.String(length=256), nullable=False),
    sa.Column('origin', sa.String(length=256), nullable=False),
    sa.Column('version', sa.String(length=256), nullable=False),
    sa.Column('overall_score', sa.Float(), nullable=True),
    sa.Column('exit_code', sa.Integer(), nullable=False),
    sa.Column('ru_utime', sa.Float(), nullable=False),
    sa.Column('ru_stime', sa.Float(), nullable=False),
    sa.Column('ru_maxrss', sa.Integer(), nullable=False),
    sa.Column('ru_ixrss', sa.Integer(), nullable=False),
    sa.Column('ru_idrss', sa.Integer(), nullable=False),
    sa.Column('ru_isrss', sa.Integer(), nullable=False),
    sa.Column('ru_minflt', sa.Integer(), nullable=False),
    sa.Column('ru_majflt', sa.Integer(), nullable=False),
    sa.Column('ru_nswap', sa.Integer(), nullable=False),
    sa.Column('ru_inblock', sa.Integer(), nullable=False),
    sa.Column('ru_oublock', sa.Integer(), nullable=False),
    sa.Column('ru_msgsnd', sa.Integer(), nullable=False),
    sa.Column('ru_msgrcv', sa.Integer(), nullable=False),
    sa.Column('ru_nsignals', sa.Integer(), nullable=False),
    sa.Column('ru_nvcsw', sa.Integer(), nullable=False),
    sa.Column('ru_nivcsw', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('inspection_run_id', sa.Integer(), nullable=False),
    sa.Column('device', sa.String(length=256), nullable=False),
    sa.Column('dtype', sa.String(length=256), nullable=False),
    sa.Column('reps', sa.Integer(), nullable=False),
    sa.Column('data_format', sa.String(length=256), nullable=False),
    sa.Column('batch', sa.Integer(), nullable=False),
    sa.Column('input_width', sa.Integer(), nullable=False),
    sa.Column('input_channels', sa.Integer(), nullable=False),
    sa.Column('filter_width', sa.Integer(), nullable=False),
    sa.Column('output_channels', sa.Integer(), nullable=False),
    sa.Column('strides', sa.Integer(), nullable=False),
    sa.Column('padding', sa.Integer(), nullable=False),
    sa.Column('elapsed', sa.Float(), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['inspection_run_id'], ['inspection_run.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pi_conv2d',
    sa.Column('component', sa.String(length=256), nullable=False),
    sa.Column('origin', sa.String(length=256), nullable=False),
    sa.Column('version', sa.String(length=256), nullable=False),
    sa.Column('overall_score', sa.Float(), nullable=True),
    sa.Column('exit_code', sa.Integer(), nullable=False),
    sa.Column('ru_utime', sa.Float(), nullable=False),
    sa.Column('ru_stime', sa.Float(), nullable=False),
    sa.Column('ru_maxrss', sa.Integer(), nullable=False),
    sa.Column('ru_ixrss', sa.Integer(), nullable=False),
    sa.Column('ru_idrss', sa.Integer(), nullable=False),
    sa.Column('ru_isrss', sa.Integer(), nullable=False),
    sa.Column('ru_minflt', sa.Integer(), nullable=False),
    sa.Column('ru_majflt', sa.Integer(), nullable=False),
    sa.Column('ru_nswap', sa.Integer(), nullable=False),
    sa.Column('ru_inblock', sa.Integer(), nullable=False),
    sa.Column('ru_oublock', sa.Integer(), nullable=False),
    sa.Column('ru_msgsnd', sa.Integer(), nullable=False),
    sa.Column('ru_msgrcv', sa.Integer(), nullable=False),
    sa.Column('ru_nsignals', sa.Integer(), nullable=False),
    sa.Column('ru_nvcsw', sa.Integer(), nullable=False),
    sa.Column('ru_nivcsw', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('inspection_run_id', sa.Integer(), nullable=False),
    sa.Column('device', sa.String(length=256), nullable=False),
    sa.Column('dtype', sa.String(length=256), nullable=False),
    sa.Column('reps', sa.Integer(), nullable=False),
    sa.Column('data_format', sa.String(length=256), nullable=False),
    sa.Column('batch', sa.Integer(), nullable=False),
    sa.Column('input_height', sa.Integer(), nullable=False),
    sa.Column('input_width', sa.Integer(), nullable=False),
    sa.Column('input_channels', sa.Integer(), nullable=False),
    sa.Column('filter_height', sa.Integer(), nullable=False),
    sa.Column('filter_width', sa.Integer(), nullable=False),
    sa.Column('output_channels', sa.Integer(), nullable=False),
    sa.Column('strides', sa.Integer(), nullable=False),
    sa.Column('padding', sa.Integer(), nullable=False),
    sa.Column('elapsed', sa.Float(), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['inspection_run_id'], ['inspection_run.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pi_matmul',
    sa.Column('component', sa.String(length=256), nullable=False),
    sa.Column('origin', sa.String(length=256), nullable=False),
    sa.Column('version', sa.String(length=256), nullable=False),
    sa.Column('overall_score', sa.Float(), nullable=True),
    sa.Column('exit_code', sa.Integer(), nullable=False),
    sa.Column('ru_utime', sa.Float(), nullable=False),
    sa.Column('ru_stime', sa.Float(), nullable=False),
    sa.Column('ru_maxrss', sa.Integer(), nullable=False),
    sa.Column('ru_ixrss', sa.Integer(), nullable=False),
    sa.Column('ru_idrss', sa.Integer(), nullable=False),
    sa.Column('ru_isrss', sa.Integer(), nullable=False),
    sa.Column('ru_minflt', sa.Integer(), nullable=False),
    sa.Column('ru_majflt', sa.Integer(), nullable=False),
    sa.Column('ru_nswap', sa.Integer(), nullable=False),
    sa.Column('ru_inblock', sa.Integer(), nullable=False),
    sa.Column('ru_oublock', sa.Integer(), nullable=False),
    sa.Column('ru_msgsnd', sa.Integer(), nullable=False),
    sa.Column('ru_msgrcv', sa.Integer(), nullable=False),
    sa.Column('ru_nsignals', sa.Integer(), nullable=False),
    sa.Column('ru_nvcsw', sa.Integer(), nullable=False),
    sa.Column('ru_nivcsw', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('inspection_run_id', sa.Integer(), nullable=False),
    sa.Column('device', sa.String(length=256), nullable=False),
    sa.Column('matrix_size', sa.Integer(), nullable=False),
    sa.Column('dtype', sa.String(length=256), nullable=False),
    sa.Column('reps', sa.Integer(), nullable=False),
    sa.Column('elapsed', sa.Float(), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['inspection_run_id'], ['inspection_run.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pi_pybench',
    sa.Column('component', sa.String(length=256), nullable=False),
    sa.Column('origin', sa.String(length=256), nullable=False),
    sa.Column('version', sa.String(length=256), nullable=False),
    sa.Column('overall_score', sa.Float(), nullable=True),
    sa.Column('exit_code', sa.Integer(), nullable=False),
    sa.Column('ru_utime', sa.Float(), nullable=False),
    sa.Column('ru_stime', sa.Float(), nullable=False),
    sa.Column('ru_maxrss', sa.Integer(), nullable=False),
    sa.Column('ru_ixrss', sa.Integer(), nullable=False),
    sa.Column('ru_idrss', sa.Integer(), nullable=False),
    sa.Column('ru_isrss', sa.Integer(), nullable=False),
    sa.Column('ru_minflt', sa.Integer(), nullable=False),
    sa.Column('ru_majflt', sa.Integer(), nullable=False),
    sa.Column('ru_nswap', sa.Integer(), nullable=False),
    sa.Column('ru_inblock', sa.Integer(), nullable=False),
    sa.Column('ru_oublock', sa.Integer(), nullable=False),
    sa.Column('ru_msgsnd', sa.Integer(), nullable=False),
    sa.Column('ru_msgrcv', sa.Integer(), nullable=False),
    sa.Column('ru_nsignals', sa.Integer(), nullable=False),
    sa.Column('ru_nvcsw', sa.Integer(), nullable=False),
    sa.Column('ru_nivcsw', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('inspection_run_id', sa.Integer(), nullable=False),
    sa.Column('rounds', sa.Integer(), nullable=False),
    sa.Column('built_in_function_calls_average', sa.Float(), nullable=False),
    sa.Column('built_in_method_lookup_average', sa.Float(), nullable=False),
    sa.Column('compare_floats_average', sa.Float(), nullable=False),
    sa.Column('compare_floats_integers_average', sa.Float(), nullable=False),
    sa.Column('compare_integers_average', sa.Float(), nullable=False),
    sa.Column('compare_interned_strings_average', sa.Float(), nullable=False),
    sa.Column('compare_longs_average', sa.Float(), nullable=False),
    sa.Column('compare_strings_average', sa.Float(), nullable=False),
    sa.Column('compare_unicode_average', sa.Float(), nullable=False),
    sa.Column('concat_strings_average', sa.Float(), nullable=False),
    sa.Column('concat_unicode_average', sa.Float(), nullable=False),
    sa.Column('create_instances_average', sa.Float(), nullable=False),
    sa.Column('create_new_instances_average', sa.Float(), nullable=False),
    sa.Column('create_strings_with_concat_average', sa.Float(), nullable=False),
    sa.Column('create_unicode_with_concat_average', sa.Float(), nullable=False),
    sa.Column('dict_creation_average', sa.Float(), nullable=False),
    sa.Column('dict_with_float_keys_average', sa.Float(), nullable=False),
    sa.Column('dict_with_integer_keys_average', sa.Float(), nullable=False),
    sa.Column('dict_with_string_keys_average', sa.Float(), nullable=False),
    sa.Column('for_loops_average', sa.Float(), nullable=False),
    sa.Column('if_then_else_average', sa.Float(), nullable=False),
    sa.Column('list_slicing_average', sa.Float(), nullable=False),
    sa.Column('nested_for_loops_average', sa.Float(), nullable=False),
    sa.Column('normal_class_attribute_average', sa.Float(), nullable=False),
    sa.Column('normal_instance_attribute_average', sa.Float(), nullable=False),
    sa.Column('python_function_calls_average', sa.Float(), nullable=False),
    sa.Column('python_method_calls_average', sa.Float(), nullable=False),
    sa.Column('recursion_average', sa.Float(), nullable=False),
    sa.Column('second_import_average', sa.Float(), nullable=False),
    sa.Column('second_package_import_average', sa.Float(), nullable=False),
    sa.Column('second_submodule_import_average', sa.Float(), nullable=False),
    sa.Column('simple_complex_arithmetic_average', sa.Float(), nullable=False),
    sa.Column('simple_dict_manipulation_average', sa.Float(), nullable=False),
    sa.Column('simple_float_arithmetic_average', sa.Float(), nullable=False),
    sa.Column('simple_int_float_arithmetic_average', sa.Float(), nullable=False),
    sa.Column('simple_integer_arithmetic_average', sa.Float(), nullable=False),
    sa.Column('simple_list_manipulation_average', sa.Float(), nullable=False),
    sa.Column('simple_long_arithmetic_average', sa.Float(), nullable=False),
    sa.Column('small_lists_average', sa.Float(), nullable=False),
    sa.Column('small_tuples_average', sa.Float(), nullable=False),
    sa.Column('special_class_attribute_average', sa.Float(), nullable=False),
    sa.Column('special_instance_attribute_average', sa.Float(), nullable=False),
    sa.Column('string_mappings_average', sa.Float(), nullable=False),
    sa.Column('string_predicates_average', sa.Float(), nullable=False),
    sa.Column('string_slicing_average', sa.Float(), nullable=False),
    sa.Column('try_except_average', sa.Float(), nullable=False),
    sa.Column('try_raise_except_average', sa.Float(), nullable=False),
    sa.Column('tuple_slicing_average', sa.Float(), nullable=False),
    sa.Column('unicode_mappings_average', sa.Float(), nullable=False),
    sa.Column('unicode_predicates_average', sa.Float(), nullable=False),
    sa.Column('unicode_properties_average', sa.Float(), nullable=False),
    sa.Column('unicode_slicing_average', sa.Float(), nullable=False),
    sa.Column('totals_average', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['inspection_run_id'], ['inspection_run.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pi_pybench')
    op.drop_table('pi_matmul')
    op.drop_table('pi_conv2d')
    op.drop_table('pi_conv1d')
    op.drop_table('has_unresolved')
    op.drop_table('has_python_requirement_lock')
    op.drop_table('advised')
    op.drop_table('provenance_checker_run')
    op.drop_table('inspection_run')
    op.drop_table('has_python_requirements')
    op.drop_table('has_external_python_requirement_lock')
    op.drop_table('has_external_python_requirement')
    op.drop_table('adviser_run')
    op.drop_table('python_software_stack')
    op.drop_table('external_python_software_stack')
    op.drop_table('python_requirements_lock')
    op.drop_table('python_requirements')
    op.drop_table('external_python_requirements_lock')
    op.drop_table('external_python_requirements')
    # ### end Alembic commands ###
