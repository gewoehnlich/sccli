from dto.tokens_dto import TokensDto


class TokensRepository:
    @classmethod
    def get(
        cls,
    ) -> Dto:
        with open(
            file = self.tokens_file,
            mode = "r",
            encoding = "utf-8",
        ) as file:
            token_data = json.loads(
                file.read().strip()
            )

        TokensDto()


    def update():
