from si_api_demo.middleware import (
    create_ecs_service,
    create_task_def,
    make_change_set,
    make_cred_region,
    create_vpc,
    run_and_log,
    create_cluster,
)

make_change_set("Infra")
make_cred_region()
vpc_data = create_vpc("demo")
run_and_log(vpc_data, "Component Sync")
cluster = create_cluster("demo")
run_and_log(cluster, "Component Sync")
task_def_si_logo = create_task_def("my-app", "keeb/si-logo", "logo")
task_def_keeb_dev = create_task_def("the-app", "keeb/keeb.dev", "blog")
run_and_log(task_def_si_logo, "Component Sync")
run_and_log(task_def_keeb_dev, "Component Sync")
mapp_data = create_ecs_service("my-app", "logo", "my-app")
tapp_data = create_ecs_service("the-app", "blog", "the-app")

run_and_log(mapp_data, "Component Sync")
run_and_log(tapp_data, "Component Sync")
