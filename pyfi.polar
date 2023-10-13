actor UserModel {}

resource ProcessorModel {
    permissions = ["read", "push", "delete"];
    roles = ["contributor", "maintainer", "admin"];

    "read" if "contributor";
    "push" if "maintainer";
    "delete" if "admin";

    "maintainer" if "admin";
    "contributor" if "maintainer";
}
allow(actor, action, resource) if has_permission(actor, action, resource);

allow(user: UserModel, "read", user2: UserModel) if
    user.name = user2.name or
    (role in user.roles and
    role.name = "admin");

allow(user: UserModel, "read", call: CallModel) if
    call.owner = user.name;

# Need to read from socket table to be able to execute task
allow(user: UserModel, "read", socket: SocketModel) if
    socket.owner = user.name or
    (role in user.roles and
    role.name = "admin");

# Privilege based access
allow(user: UserModel, "read", log: LogModel) if
    log.public = true and
    has_privilege(user, "READ_LOG", log);

allow(user: UserModel, "read", processor: ProcessorModel) if
    has_role(user, "contributor", processor);    
  
has_privilege(actor: UserModel, priv_name: String, _: LogModel) if
  (privilege in actor.privileges and
  privilege.name = priv_name) or
  (role in actor.roles and
  priv in role.privileges and
  priv.name = priv_name);

has_role(actor: UserModel, role_name: String, _: ProcessorModel) if
  role in actor.roles and
  role.name = role_name;

allow(_: UserModel, "read", _: PasswordModel);
allow(_: UserModel, "read", _: WorkerModel);
allow(_: UserModel, "read", _: PrivilegeModel);
allow(_: UserModel, "read", _: AgentModel);
allow(_: UserModel, "read", _: FileModel);
allow(_: UserModel, "read", _: EventModel);
allow(_: UserModel, "read", _: NodeModel);
allow(_: UserModel, "read", _: PlugModel);
allow(_: UserModel, "read", _: TaskModel);
allow(_: UserModel, "read", _: CallModel);
allow(_: UserModel, "read", _: LogModel);
allow(_: UserModel, "read", _: QueueModel);
allow(_: UserModel, "read", _: SocketModel);
allow(_: UserModel, "read", _: RoleModel);
allow(_: UserModel, "read", _: SchedulerModel);
allow(_: UserModel, "read", _: ArgumentModel);
allow(_: UserModel, "read", _: DeploymentModel);
allow(_: UserModel, "read", _: NetworkModel);
