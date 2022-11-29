from pydantic import BaseModel


class Benefit(BaseModel):
    name: str
    slug: str or None = None

    def benefit_to_dict(self):
        return vars(self)


def BenefitResult(benefit) -> dict:
    return {
        "id": benefit[0],
        "name": benefit[1],
        "slug": benefit[2]
    }


def BenefitListResult(benefits) -> list:
    return [BenefitResult(benefit) for benefit in benefits]


