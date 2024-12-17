from singer_sdk.typing import (
    ArrayType,
    BooleanType,
    DateTimeType,
    IntegerType,
    ObjectType,
    PropertiesList,
    Property,
    StringType,
)


event_properties = PropertiesList(
    Property(
        "ResourceId",
        StringType,
        required=True,
        description="The unique identifier of the event."

    ),
    Property(
        "Date",
        IntegerType,
        description="The date and time the event occured."

    ),
    Property(
        "EventType",
        StringType,
        description="The type of the event."
    )
)

payins_properties = PropertiesList(

    Property(
        "Id",
        StringType,
        required=True,
        description="The unique identifier of the object."
    ),
    Property(
        "Tag",
        StringType,
        description="Custom data that you can add to this object. For transactions (pay-in, transfer, payout), "
                    "you can use this parameter to identify corresponding information regarding the user, transaction, "
                    "or payment methods on your platform."
    ),
    Property(
        "CreationDate",
        IntegerType,
        description="The date and time at which the object was created."
    ),
    Property(
        "Author_id",
        StringType,
        description="The unique identifier of the user at the source of the transaction."
    ),
    Property(
        "CreditedUserId",
        StringType,
        description="The unique identifier of the user whose wallet is credited."
    ),
    Property(
        "CreditedFunds",
        ObjectType(
            Property(
                "Currency",
                StringType,
                description="The currency of the debited funds (the sell currency)."
            ),
            Property(
                "Amount",
                IntegerType,
                description="An amount of money in the smallest sub-division of the currency "
            )
        ),
        description="Information about the credited funds (CreditedFunds = DebitedFunds - Fees)."
    ),
    Property(
        "DebitedFunds",
        ObjectType(
            Property(
                "Currency",
                StringType,
                description="The currency of the debited funds (the sell currency)."
            ),
            Property(
                "Amount",
                IntegerType,
                description="An amount of money in the smallest sub-division of the currency "
            )
        ),
        description="Information about the debited funds."
    ),
    Property(
        "Fees",
        ObjectType(
            Property(
                "Currency",
                StringType,
                description="The currency of the debited funds (the sell currency)."
            ),
            Property(
                "Amount",
                IntegerType,
                description="An amount of money in the smallest sub-division of the currency "
            )
        ),
        description="Information about the fees taken by the platform for this transaction"
                    " (and hence transferred to the Fees Wallet)."
    ),
    Property(
        "Status",
        StringType,
        description="The status of the transaction."
    ),
    Property(
        "ResultCode",
        StringType,
        description="The code indicating the result of the operation. This information is mostly used to handle "
                    "errors or for filtering purposes."
    ),
    Property(
        "ResultMessage",
        DateTimeType,
        description="The date and time at which the status changed to SUCCEEDED, indicating that the transaction"
                    " occurred. The statuses CREATED and FAILED return an ExecutionDate of null."
    ),
    Property(
        "Type",
        StringType,
        description="The type of transaction."
    ),
    Property(
        "Nature",
        StringType,
        description="The nature of the transaction, providing more information about the context in which "
                    "the transaction occurred:"
    ),
    Property(
        "PaymentType",
        StringType,
        description="The type of pay-in."
    ),
    Property(
        "CreditedWalletId",
        StringType,
        description="The unique identifier of the credited wallet."
    ),
    Property(
        "DebitedWalletId",
        StringType,
        description="The unique identifier of the debited wallet."
    )
)


refunds_properties = PropertiesList(
    Property(
        "Id",
        StringType,
        required=True,
        description="The unique identifier of the object."
    ),
    Property(
        "Tag",
        StringType,
        description="Custom data that you can add to this object. For transactions (pay-in, transfer, payout), "
                    "you can use this parameter to identify corresponding information regarding the user, transaction, "
                    "or payment methods on your platform."
    ),
    Property(
        "CreationDate",
        IntegerType,
        description="The date and time at which the object was created."
    ),
    Property(
        "AuthorId",
        StringType,
        description="The unique identifier of the user at the source of the initial transaction."
    ),
    Property(
        "CreditedUserId",
        StringType,
        description="The unique identifier of the user whose wallet is credited."
    ),
    Property(
        "DebitedFunds",
        ObjectType(
            Property(
                "Amount",
                IntegerType,
                description="An amount of money in the smallest sub-division of the currency "
            ),
            Property(
                "Currency",
                StringType,
                description="The currency of the debited funds (the sell currency)."
            )
        ),
        description="Information about the debited funds."
    ),
    Property(
        "CreditedFunds",
        ObjectType(
            Property(
                "Currency",
                StringType,
                description="The currency of the debited funds (the sell currency)."
            ),
            Property(
                "Amount",
                IntegerType,
                description="An amount of money in the smallest sub-division of the currency "
            )
        ),
        description="Information about the credited funds (CreditedFunds = DebitedFunds - Fees)."
    ),
    Property(
        "Fees",
        ObjectType(
            Property(
                "Currency",
                StringType,
                description="The currency of the debited funds (the sell currency)."
            ),
            Property(
                "Amount",
                IntegerType,
                description="An amount of money in the smallest sub-division of the currency "
            )
        ),
        description="Information about the fees taken by the platform for this transaction (and hence transferred "
                    "to the Fees Wallet)."
    ),
    Property(
        "Status",
        StringType,
        description="The status of the transaction."
    ),
    Property(
        "ResultCode",
        StringType,
        description="The code indicating the result of the operation. This information is mostly used to handle "
                    "errors or for filtering purposes."
    ),
    Property(
        "ResultMessage",
        StringType,
        description="The explanation of the result code."
    ),
    Property(
        "ExecutionDate",
        IntegerType,
        description="The date and time at which the status changed to SUCCEEDED, indicating that the transaction "
                    "occurred. The statuses CREATED and FAILED return an ExecutionDate of null."
    ),
    Property(
        "Type",
        StringType,
        description="The type of the transaction."
    ),
    Property(
        "Nature",
        StringType,
        description="The nature of the transaction, providing more information about the context in "
                    "which the transaction occurred (values accepted : REGULAR, REPUDIATION, REFUND, SETTLEMENT) "
    ),
    Property(
        "InitialTransactionId",
        StringType,
        description="The unique identifier of the initial transaction being refunded."
    ),
    Property(
        "InitialTransactionType",
        StringType,
        description="The type of the initial transaction being refunded. (values accepted : PAYIN, TRANSFER, PAYOUT) "
    ),
    Property(
        "InitialTransactionNature",
        StringType,
        description=" The nature of the initial transaction being refunded, providing more information about "
                    "the context in which the transaction occurred "
                    "(values accepted : REGULAR, REPUDIATION, REFUND, SETTLEMENT)"
    ),
    Property(
        "DebitedWalletId",
        StringType,
        description="The unique identifier of the debited wallet."
    ),
    Property(
        "CreditedWalletId",
        StringType,
        description="The unique identifier of the credited wallet."
    ),
    Property(
        "RefundReason",
        ObjectType(
            Property(
                "RefundReasonMessage",
                StringType,
                description="Message explaining the reason for the refusal."
            ),
            Property(
                "RefundReasonType",
                StringType,
                description="The type of reason for the refund (INITIALIZED_BY_CLIENT, BANKACCOUNT_INCORRECT, "
                            "OWNER_DO_NOT_MATCH_BANKACCOUNT, BANKACCOUNT_HAS_BEEN_CLOSED,"
                            " WITHDRAWAL_IMPOSSIBLE_ON_SAVINGS_ACCOUNTS, OTHER)"
            )
        ),
    ),
    Property(
        "StatementDescriptor",
        StringType,
        description="Custom description to appear on the user’s bank statement along with the platform name. "
                    "Different banks may show more or less information. See the Customizing bank statement references"
                    " article for details."
    )
)


payouts_properties = PropertiesList(
    Property(
        "Id",
        StringType,
        description="The unique identifier of the object."
    ),
    Property(
        "Tag",
        StringType,
        description="Custom data that you can add to this object. For transactions (pay-in, transfer, payout), "
                    "you can use this parameter to identify corresponding information regarding the user, transaction, "
                    "or payment methods on your platform."
    ),
    Property(
        "CreationDate",
        IntegerType,
        description="The date and time at which the object was created."
    ),
    Property(
        "AuthorId",
        StringType,
        description="The unique identifier of the user at the source of the initial transaction."
    ),
    Property(
        "CreditedUserId",
        StringType,
        description="The unique identifier of the user whose wallet is credited."
    ),
    Property(
        "DebitedFunds",
        ObjectType(
            Property(
                "Currency",
                StringType,
                description="The currency of the debited funds (the sell currency)."
            ),
            Property(
                "Amount",
                IntegerType,
                description="An amount of money in the smallest sub-division of the currency "
            )
        ),
        description="Information about the debited funds."
    ),
    Property(
        "CreditedFunds",
        ObjectType(
            Property(
                "Currency",
                StringType,
                description="The currency of the debited funds (the sell currency)."
            ),
            Property(
                "Amount",
                IntegerType,
                description="An amount of money in the smallest sub-division of the currency "
            )
        ),
        description="Information about the credited funds (CreditedFunds = DebitedFunds - Fees)."
    ),
    Property(
        "Fees",
        ObjectType(
            Property(
                "Currency",
                StringType,
                description="The currency of the debited funds (the sell currency)."
            ),
            Property(
                "Amount",
                IntegerType,
                description="An amount of money in the smallest sub-division of the currency "
            )
        ),
        description="Information about the fees taken by the platform for this transaction (and hence transferred to "
                    "the Fees Wallet)."
    ),
    Property(
        "Status",
        StringType,
        description="The status of the transaction (values accepted = CREATED, SUCCEEDED, FAILED)"
    ),
    Property(
        "ResultCode",
        StringType,
        description="The code indicating the result of the operation. This information is mostly used to handle errors "
                    "or for filtering purposes."
    ),
    Property(
        "ResultMessage",
        StringType,
        description="The explanation of the result code."
    ),
    Property(
        "ExecutionDate",
        IntegerType,
        description="The date and time at which the status changed to SUCCEEDED, indicating that the transaction "
                    "occurred. The statuses CREATED and FAILED return an ExecutionDate of null."
    ),
    Property(
        "Type",
        StringType,
        description="The type of the transaction : Returned values: PAYIN, TRANSFER, CONVERSION, PAYOUT"
    ),
    Property(
        "Nature",
        StringType,
        description=" The nature of the transaction, providing more information about the context in which the "
                    "transaction occurred : Returned values: REGULAR, REPUDIATION, REFUND, SETTLEMENT"
    ),
    Property(
        "CreditedWalletId",
        StringType,
        description="The unique identifier of the credited wallet. In the specific case of the Payout object, "
                    "This value is always null since there is no credited wallet."
    ),
    Property(
        "DebitedWalletId",
        StringType,
        description="The unique identifier of the debited wallet."
    ),
    Property(
        "PaymentType",
        StringType,
        description="The type of pay-in : Returned values: CARD, DIRECT_DEBIT, PREAUTHORIZED, BANK_WIRE"
    ),
    Property(
        "BankAccountId",
        StringType,
        description="The unique identifier of the bank account."
    ),
    Property(
        "BankWireRef",
        StringType,
        description="Custom description to appear on the user’s bank statement along with the platform name. "
                    "The recommended length is 12 characters – strings longer than this may be truncated "
                    "depending on the bank."
    )
)

transfers_properties = PropertiesList(
    Property(
        "Id",
        StringType,
        description="The unique identifier of the object."
    ),
    Property(
        "Tag",
        StringType,
        description="Custom data that you can add to this object"
    ),
    Property(
        "CreationDate",
        IntegerType,
        description="The date and time at which the object was created."
    ),
    Property(
        "AuthorId",
        StringType,
        description="The unique identifier of the user at the source of the initial transaction."
    ),
    Property(
        "CreditedUserId",
        StringType,
        description="The unique identifier of the user whose wallet is credited."
    ),
    Property(
        "DebitedFunds",
        ObjectType(
            Property(
                "Currency",
                StringType,
                description="The currency of the debited funds (the sell currency)."
            ),
            Property(
                "Amount",
                IntegerType,
                description="An amount of money in the smallest sub-division of the currency "
            )
        ),
        description="Information about the debited funds."
    ),
    Property(
        "CreditedFunds",
        ObjectType(
            Property(
                "Currency",
                StringType,
                description="The currency of the debited funds (the sell currency)."
            ),
            Property(
                "Amount",
                IntegerType,
                description="An amount of money in the smallest sub-division of the currency "
            )
        ),
        description="Information about the credited funds (CreditedFunds = DebitedFunds - Fees)."
    ),
    Property(
        "Fees",
        ObjectType(
            Property(
                "Currency",
                StringType,
                description="The currency of the debited funds (the sell currency)."
            ),
            Property(
                "Amount",
                IntegerType,
                description="An amount of money in the smallest sub-division of the currency "
            )
        ),
        description="Information about the fees taken by the platform for this transaction (and hence transferred "
                    "to the Fees Wallet)."
    ),
    Property(
        "Status",
        StringType,
        description="The status of the transaction (values accepted = CREATED, SUCCEEDED, FAILED)"
    ),
    Property(
        "ResultCode",
        StringType,
        description="The code indicating the result of the operation. This information is mostly used to handle "
                    "errors or for filtering purposes."
    ),
    Property(
        "ResultMessage",
        StringType,
        description="The explanation of the result code."
    ),
    Property(
        "ExecutionDate",
        IntegerType,
        description="The date and time at which the status changed to SUCCEEDED, indicating that the transaction "
                    "occurred. The statuses CREATED and FAILED return an ExecutionDate of null."
    ),
    Property(
        "Type",
        StringType,
        description="The type of the transaction : Returned values: PAYIN, TRANSFER, CONVERSION, PAYOUT"
    ),
    Property(
        "Nature",
        StringType,
        description=" The nature of the transaction, providing more information about the context in which the "
                    "transaction occurred : Returned values: REGULAR, REPUDIATION, REFUND, SETTLEMENT"
    ),
    Property(
        "CreditedWalletId",
        StringType,
        description="The unique identifier of the credited wallet. In the specific case of the Payout object, "
                    "This value is always null since there is no credited wallet."
    ),
    Property(
        "DebitedWalletId",
        StringType,
        description="The unique identifier of the debited wallet."
    ),
)

users_properties = PropertiesList(
    Property(
        "Id",
        StringType,
        description="The unique identifier of the object."
    ),
    Property(
        "Tag",
        StringType,
        description="Custom data that you can add to this object."
    ),
    Property(
        "CreationDate",
        IntegerType,
        description="The date and time at which the object was created."
    ),
    Property(
        "PersonType",
        StringType,
        description="The type of the user: NATURAL – Natural users are individuals (natural persons). LEGAL – Legal "
                    "users are legal entities (legal persons) like companies, non-profits, and sole proprietors."
    ),
    Property(
        "Email",
        StringType,
        description="The email address of the user."
    ),
    Property(
        "KYCLevel",
        StringType,
        description="The verification status of the user set by Mangopay (LIGHT or REGULAR)"
    ),
    Property(
        "TermsAndConditionsAccepted",
        BooleanType,
        description="Whether the user has accepted Mangopay’s terms and conditions (as defined by your contract). "
                    "If this value is not true, Owners will be limited in their use of Mangopay."
    ),
    Property(
        "TermsAndConditionsAcceptedDate",
        IntegerType,
        description="The date and time at which the TermsAndConditionsAccepted value was set to true"
    ),
    Property(
        "UserCategory",
        StringType,
        description="he category of the user: PAYER – User who can only make pay-ins to their wallet and transfers "
                    "to other wallets. OWNER – User who can do everything a Payer can, plus receive transfers to their "
                    "wallet. To request payouts, an Owner user’s KYCLevel must be REGULAR. For more information,"
    ),
    Property(
        "UserStatus",
        StringType,
        description="Internal use only. This field can only be used and updated by Mangopay teams. (ACTIVE or CLOSED) "
    )
)

bankaccount_properties = PropertiesList(
    Property(
        "OwnerAddress",
        ObjectType(
            Property(
                "AddressLine1",
                StringType,
                description="The first line of the address."
            ),
            Property(
                "AddressLine2",
                StringType,
                description="The second line of the address."
            ),
            Property(
                "City",
                StringType,
                description="The city of the address."
            ),
            Property(
                "Region",
                StringType,
                description="The region of the address."
            ),
            Property(
                "PostalCode",
                StringType,
                description="The postal code of the address. The postal code can contain the following characters: alphanumeric, dashes, and spaces."
            ),
            Property(
                "Country",
                StringType,
                description="Two-letter country code (ISO 3166-1 alpha-2 format)."
            ),
        ),
        description="Information about the address of residence of the bank account owner."
    ),
    Property(
        "IBAN",
        StringType,
        description="The IBAN (international bank account number) of the bank account."
    ),
    Property(
        "BIC",
        StringType,
        description="The BIC (international identifier of the bank) for IBAN or OTHER-type bank accounts."
    ),
    Property(
        "AccountNumber",
        StringType,
        description="The unique set of digits of the bank account."
    ),
    Property(
        "SortCode",
        StringType,
        description="The 6-digit sort code, assigned to UK financial institutions, for GB-type bank accounts."
    ),
    Property(
        "UserId",
        StringType,
        description="The unique identifier of the User (natural or legal) who owns the bank account."
    ),
    Property(
        "OwnerName",
        StringType,
        description="The full name of the owner of the bank account. (Format: FirstName LastName)"
    ),
    Property(
        "Type",
        StringType,
        description="The type of the bank account, indicating the country where the real-life account is registered  (IBAN, US, CA, GB, OTHERS)"
    ),
    Property(
        "Id",
        StringType,
        description="The unique identifier of the object."
    ),
    Property(
        "Tag",
        StringType,
        description="Custom data that you can add to this object."
    ),
    Property(
        "CreationDate",
        IntegerType,
        description="The date and time at which the object was created."
    ),
    Property(
        "Active",
        BooleanType,
        description="Whether or not the Bank Account is active."
    )
)


kyc_properties = PropertiesList(
    Property(
        "Type",
        StringType,
        description="The type of the document for the user verification"
    ),
    Property(
        "UserId",
        StringType,
        description="The unique identifier of the user."
    ),
    Property(   
        "Flags",
        ArrayType(StringType),
        description="The flags of the document for the user verification"
    ),
    Property(
        "Id",
        StringType,
        description="The unique identifier of the object."
    ),
    Property(
        "Tag",
        StringType,
        description="Custom data that you can add to this object."
    ),
    Property(
        "CreationDate",
        IntegerType,
        description="The date and time at which the object was created."
    ),
    Property(
        "ProcessedDate",
        IntegerType,
        description="The date and time at which the document was processed by Mangopay’s team."
    ),
    Property(
        "Status",   
        StringType,
        description="The status of the document for the user verification"
    ),
    Property(
        "RefusedReasonType",
        StringType,
        description="The type of reason for the refusal of the document for the user verification"
    ),
    Property(
        "RefusedReasonMessage",
        StringType,
        description="The message of the reason for the refusal of the document for the user verification"
    )
)


wallet_properties = PropertiesList(
    Property(
        "Description",
        StringType,
        description="The description of the wallet. It can be a name, the type, or anything else that can help you clearly identify the wallet on the platform (and for your end users)."
    ),
    Property(
        "Owners",
       ArrayType(StringType),
        description="The unique identifier of the user owning the wallet"
    ),
    Property(
        "Balance",
        ObjectType(
            Property(
                "Currency",
                StringType,
                description="The currency of the wallet."
            ),
            Property(
                "Amount",
                IntegerType,
                description="The amount of money in the wallet."
            )   
        ),
        description="The current balance of the wallet."
    ),
    Property(
        "Currency",
        StringType,
        description="The currency of the wallet."
    ),
    Property(
        "FundsType",
        StringType,
        description="The type of funds in the wallet:"
    ),
    Property(
        "Id",
        StringType,
        description="The unique identifier of the object."
    ),
    Property(
        "Tag",
        StringType,
        description="Custom data that you can add to this object."
    ),
    Property(
        "CreationDate",
        IntegerType,
        description="The date and time at which the object was created."
    )
)