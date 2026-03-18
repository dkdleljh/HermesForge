from app.policies.safety_kernel import SafetyKernel


class PolicyService:
    def __init__(self):
        self.kernel = SafetyKernel()

    def get_policy(self):
        return self.kernel.rules()
