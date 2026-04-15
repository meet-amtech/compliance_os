class Tenant(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50)
    plan = models.CharField(max_length=50)
    timezone = models.CharField(max_length=50)
    settings_json = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=50)
    last_login_at = models.DateTimeField(null=True, blank=True)

class Framework(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    source_type = models.CharField(max_length=50)

    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=50)

class Obligation(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField()

    reference_code = models.CharField(max_length=100)
    severity = models.CharField(max_length=50)
    periodicity = models.CharField(max_length=50)

    due_rule_json = models.JSONField(default=dict)

    status = models.CharField(max_length=50)

    class Control(models.Model):
        tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
        framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
        obligation = models.ForeignKey(Obligation, on_delete=models.CASCADE)

        owner_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

        control_type = models.CharField(max_length=50)
        frequency = models.CharField(max_length=50)
        risk_level = models.CharField(max_length=50)

        effectiveness_score = models.FloatField(null=True, blank=True)

        status = models.CharField(max_length=50)

        class Task(models.Model):
            tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

            title = models.CharField(max_length=255)
            description = models.TextField()

            source_type = models.CharField(max_length=50)
            source_id = models.IntegerField()

            owner_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

            workflow_id = models.IntegerField(null=True, blank=True)

            priority = models.CharField(max_length=50)
            due_date = models.DateTimeField()

            status = models.CharField(max_length=50)
            recurrence_pattern = models.JSONField(default=dict)

            created_by = models.ForeignKey(User, related_name='created_tasks', on_delete=models.SET_NULL, null=True)

            class Evidence(models.Model):
                tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

                task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
                control = models.ForeignKey(Control, on_delete=models.CASCADE, null=True, blank=True)

                document_id = models.IntegerField()

                evidence_type = models.CharField(max_length=50)

                validity_from = models.DateField()
                validity_to = models.DateField()

                reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

                review_status = models.CharField(max_length=50)

                class AuditLog(models.Model):
                    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

                    entity_type = models.CharField(max_length=100)
                    entity_id = models.IntegerField()

                    action = models.CharField(max_length=50)

                    old_data_json = models.JSONField(default=dict)
                    new_data_json = models.JSONField(default=dict)

                    actor_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

                    created_at = models.DateTimeField(auto_now_add=True)

class BaseModel(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

        STATUS_CHOICES = [
            ("active", "Active"),
            ("inactive", "Inactive"),
        ]

        class Meta:
            indexes = [
                models.Index(fields=["tenant"]),
            ]

            queryset.filter(tenant=request.user.tenant)