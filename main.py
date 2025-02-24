import requests
import json


def hit_rest_api(url, data, method):
    try:
        headers = {'Content-Type': 'application/json'}
        if method == "POST":
            response = requests.post(url, headers=headers, data=json.dumps(data))
        elif method == "PUT":
            response = requests.put(url, headers=headers, data=json.dumps(data))

        # print(response.status_code)
        if response.status_code != 200:
            print(response.json())
            exit(0)
        response.raise_for_status()  # Raise an error for non-2xx responses
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error while requesting {url}: {e}")
        exit(0)
        return None


def main():
    udb_id = "retail_buy_4"
    # base_url = "https://health-insurance-sureos-dev.internal.ackodev.com"
    base_url = "http://127.0.0.1:5015"

    # Create an EMPTY UDB
    # response = hit_rest_api("https://sureos-input-data-capture.ackosureosuat.com/acko/v1/input-data-capture", {
    #     "input_data_id": udb_id,
    #     "input_data": {}
    # }, "POST")

    print("new MJ created with UDB id - " + udb_id)
    print()

    # Initial MEGA JSON
    mega_json = {
        "udb": {
            "udb_id": udb_id,
            "channel": "retail",
            "zone": "1",
            "users": [
                {
                    "user_id": "1234",
                    "name": "pon",
                    "pincode": "560100",
                    "role": "proposer",
                    "phone": "9894955622",
                    "age": 30
                },
                {
                    "user_id": "12345",
                    "name": "jitesh",
                    "pincode": "560100",
                    "role": "insured",
                    "relationship": "self",
                    "phone": "9894955622",
                    "credit_score": 750,
                    "age": 30
                }
            ],
            "risk_profile": [
                {
                    "entity_id": "fWJuYJSkR70Mh3ICbNHWDQ",
                    "name": "Credit",
                    "risk_attributes": [
                        {
                            "key": "creditScore",
                            "status": "complete",
                            "updatedOn": "2023-12-07T18:18:45.197736",
                            "validTill": "2024-06-07",
                            "value": "7"
                        }
                    ],
                    "type": "Credit"
                }
            ],

            "insureds":
                [],
            "recommended_plans":
                [],
            "selected_plans": [
                {
                    "parameters": {
                        "sum_insured": {
                            "id": "sum_insured",
                            "value": 4000000
                        }
                    },
                    "sellable_plan_id": "acko_retail_platinum_plan"
                }
            ],
            "eligibility":
                {},
            "plans":
                [],
            "financial_data":
                {},
            "medical_data":
                {}
        },
        "prospect":
            {
                "eligibile_plans":
                    [
                        {
                            "plan_parmaeters":
                                {},
                            "clause_parameters":
                                {},
                            "cover_parameters":
                                {},
                            "insured_parameters":
                                {}
                        }
                    ],
                "selected_plans":
                    [
                        {
                            "plan_parmaeters":
                                {},
                            "clause_parameters":
                                {},
                            "cover_parameters":
                                {},
                            "insured_parameters":
                                {}
                        }
                    ],
                "eligibility":
                    {},
                "quote_details": {

                }
            },
        "proposals": {
            "plans":
                [],
            "users":
                [],
            "insureds":
                [],
            "orders":
                [],
            "quotes":
                [],
            "communication":
                {}
        }
        ,
        "risk_profile":
            {
                "risk_factors_to_be_filled":
                    {},
                "financial_data":
                    {},
                "medical":
                    {}
            },
        "fulfilment":
            {
                "fraud":
                    {},
                "kyc":
                    {}
            }
    }

    # Data Collection
    # Plan recommendation

    api_endpoints = [
        {
            "url": base_url + "/api/v1/data-collection/node", "data":
            {
                "before": {},
                "execute": {
                    "bos": [
                        {
                            "input_transform": [
                                {
                                    "operation": "shift",
                                    "spec": {
                                        "@": "."
                                    }
                                }
                            ]
                        }
                    ],
                    "control": [
                        {
                            "value": "*",
                            "step": "dataEnrichment"
                        }
                    ]
                },
                "after": {}
            }
        },
        {
            "url": base_url + "/api/v1/data-sufficiency/node", "data":
            {

                "before": {},
                "execute": {
                    "bos": [
                        {
                            "input_transform": [
                                {
                                    "operation": "shift",
                                    "spec": {
                                        "udb": {
                                            "users": {
                                                "0": "."
                                            },
                                            "channel": "channel"
                                        }
                                    }
                                }
                            ],
                            "method": "POST",
                            "path": base_url + "/api/v1/data-collection/sufficiency",
                            "output_transform": [
                                {
                                    "operation": "shift",
                                    "spec": {
                                        "required_fields": "required_fields",
                                        "data_sufficient": "data_sufficient"
                                    }
                                }
                            ]
                        }
                    ],
                    "control": [
                        {
                            "key": "data_sufficient",
                            "value": "false",
                            "step": "dataCollection"
                        },
                        {
                            "key": "data_sufficient",
                            "value": "true",
                            "step": "eligibility"
                        }
                    ]
                },
                "after": {}
            }
        },
        {
            "url": base_url + "/api/v1/data-enrichment/node", "data":
            {

                "before": {},
                "execute": {
                    "bos": [
                        {
                            "input_transform": [
                                {
                                    "operation": "shift",
                                    "spec": {
                                        "required_fields": "requested_fields",
                                        "udb": {
                                            "users": {
                                                "0": "context"
                                            }
                                        }
                                    }
                                }
                            ],
                            "method": "POST",
                            "path": "http://127.0.0.1:5015/api/v1/data-collection/enrich",
                            "output_transform": [
                                {
                                    "operation": "shift",
                                    "spec": {
                                        "context": {
                                            "@": "udb.users[0]",
                                            "zone": "udb.zone"
                                        }
                                    }
                                }
                            ]
                        }
                    ],
                    "control": [
                        {
                            "value": "*",
                            "step": "dataSufficiency"
                        }
                    ]
                },
                "after": {},
                "result": {
                    "prospect": {
                        "eligibile_plans": [
                            {
                                "plan_parmaeters": {},
                                "clause_parameters": {},
                                "cover_parameters": {},
                                "insured_parameters": {}
                            }
                        ],
                        "selected_plans": [
                            {
                                "plan_parmaeters": {},
                                "clause_parameters": {},
                                "cover_parameters": {},
                                "insured_parameters": {}
                            }
                        ],
                        "eligibility": {},
                        "quote_details": {}
                    },
                    "udb": {
                        "udb_id": "1",
                        "channel": "retail",
                        "users": [
                            {
                                "user_id": "1234",
                                "name": "pon",
                                "pincode": "560100",
                                "role": "proposer",
                                "phone": "9894955622",
                                "age": 30
                            },
                            {
                                "user_id": "12345",
                                "name": "jitesh",
                                "pincode": "560100",
                                "role": "insured",
                                "relationship": "self",
                                "phone": "9894955622",
                                "age": 30
                            }
                        ],
                        "insureds": [],
                        "recommended_plans": [],
                        "selected_plans": [
                            {
                                "parameters": {
                                    "sum_insured": {
                                        "id": "sum_insured",
                                        "value": 4000000
                                    }
                                },
                                "sellable_plan_id": "acko_retail_platinum_plan"
                            }
                        ],
                        "eligibility": {},
                        "plans": [],
                        "financial_data": {},
                        "medical_data": {}
                    },
                    "next_node": "dataCollection",
                    "risk_profile": {
                        "risk_factors_to_be_filled": {},
                        "financial_data": {},
                        "medical": {}
                    },
                    "proposals": {
                        "plans": [],
                        "users": [],
                        "insureds": [],
                        "orders": [],
                        "quotes": [],
                        "communication": {}
                    },
                    "fulfilment": {
                        "fraud": {},
                        "kyc": {}
                    },
                    "required_fields": [
                        "credit_score",
                        "zone"
                    ],
                    "data_sufficient": "false"
                }
            }

        },
        {
            "url": base_url + "/api/v1/node/fulfil-lr", "data":
            {

                "bos": [
                    {
                        "before_transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/configuration/fulfilment_lr.json",
                            "set_path": "false"

                        },
                        "binterface": "fulfilment_lr_attributes",
                        "path": "v1/",
                        "path_variable": "",
                        "role": "output",
                        "name": "fulfilment_lr_attributes",
                        "method": "POST",
                    }
                ],
                "control": {
                    "value": "unfulfilled",
                    "key": "fulfilment_lr",
                    "transformer": {
                        "type": "JOLT",
                        "resource_file_path": "specs/configuration/fulfilment_control.json"
                    },
                    "node": "eligibitlity_status"
                }
            }

        },
        {
            "url": base_url + "/api/v1/eligibilityasa/checkEligibility", "data":
            {
                "bos": [
                    {
                        "before_transformer": {
                            "type": "JOLT",
                            "resource_file_path": "/specs/ACKO_HEALTH_LR_ELIGIBILITY_input_specs_jolt.json"
                        },
                        "binterface": "checkEligibility",
                        "path": "/api/v1/eligibility",
                        "path_variable": "udbId",
                        "filters": {
                            "directory_location": "/acko/health/design",
                            "eligibility_rule_id": "ACKO_HEALTH_LR_ELIGIBILITY"
                        },
                        "after_transformer": {
                            "type": "JOLT",
                            "resource_file_path": "/specs/ACKO_HEALTH_LR_ELIGIBILITY_output_specs_jolt.json"
                        },
                        "role": "getRiskProfile",
                        "name": "udb",
                        "method": "GET"
                    }
                ]
            }
        },
        {
            "url": base_url + "/api/v1/eligibilityasa/determineNextStep", "data":
            {
                "bos": [
                    {
                        "before_transformer": {
                            "type": "JOLT",
                            "resource_file_path": "/specs/ACKO_HEALTH_LR_ELIGIBILITY_return_specs_jolt.json"
                        },
                        "binterface": "determineNextStep",
                        "path": "/api/v1/eligibility",
                        "path_variable": "udbId",
                        "filters": {
                            "directory_location": "/acko/health/design",
                            "eligibility_rule_id": "ACKO_HEALTH_LR_ELIGIBILITY"
                        },
                        "role": "determineNextStep",
                        "name": "udb",
                        "method": "GET"
                    }
                ],
                "controller": [
                    {
                        "json_transformer": "/specs/ACKO_HEALTH_LR_ELIGIBILITY_return_specs_jolt.json",
                        "value": "Accept",
                        "nextStep": "NEXT_STEP"
                    },
                    {
                        "json_transformer": "/specs/ACKO_HEALTH_LR_ELIGIBILITY_return_specs_jolt.json",
                        "value": "Reject",
                        "nextStep": "DROP_OFF"
                    }
                ]
            }
        },
        {
            "url": base_url + "/api/v1/node/plan-recommend/get", "data":
            {
                "before": {},
                "execute": {
                    "bos": [
                        {
                            "input_transform": [
                                {
                                    "operation": "shift",
                                    "spec": {
                                        "udb": {
                                            "zone": "zone",
                                            "channel": "channel",
                                            "users": {
                                                "*": {
                                                    "role": {
                                                        "proposer": {
                                                            "@(2,age)": "age",
                                                            "@(2,credit_score)": "credit_score"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            ],
                            "host": "https://eligibility-rule-engine.ackosureosuat.com",
                            "path_variable": "/rules/plan_recommendation_rule/evaluate",
                            "method": "POST",
                            "headers": {
                                "directory-location": "/acko/health/design"
                            },
                            "request": {},
                            "output_transform": [
                                {
                                    "operation": "shift",
                                    "spec": {
                                        "response": {
                                            "result": {
                                                "0": {
                                                    "sellable_plan_id": "prospect.recommended_plans[0].sellable_plan_id",
                                                    "base_sum_insured_list": "prospect.recommended_plans[0].parameters.base_sum_insured_list"
                                                }
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                },
                "after": {}
            }
        },
        {
            "url": base_url + "/api/v1/node/empty-proposal/validate/execute-node", "data":
            {
                "before": {
                    "bos": [],
                    "control": {
                        "transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/configuration/empty_proposal_validate_before_decision.json"

                        },
                        "step": "execute"
                    }
                },
                "execute": {
                    "bos": [
                        {
                            "before_transformer": {
                                "type": "JOLT",
                                "resource_file_path": "specs/configuration/empty-proposal-validation.json"
                            },

                            "binterface": "proposal",
                            "path": "/v1/",
                            "path_variable": "",
                            "role": "output",
                            "name": "validate-proposal",
                            "method": "validate"
                        }
                    ]
                },
                "after": {
                    "bos": [],
                    "control": {
                        "transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/configuration/empty_proposal_after_decision.json"
                        },
                        "step": "proposal-insured"
                    }
                }

            }
        },
        {
            "url": base_url + "/api/v1/node/empty-proposal/create/execute-node", "data":
            {
                "before": {
                    "bos": [],
                    "control": {
                        "transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/configuration/empty_proposal_before_decision.json"
                        },
                        "step": "execute"
                    }
                },
                "execute": {
                    "bos": [
                        {
                            "before_transformer": {
                                "type": "JOLT",
                                "resource_file_path": "specs/configuration/proposal_user.json"
                            },
                            "binterface": "proposal",
                            "path": "/v1/",
                            "path_variable": "",
                            "role": "output",
                            "name": "proposals",
                            "method": "POST"
                        }
                    ],
                    "control": {
                        "transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/configuration/empty_proposal_execute_decision.json"
                        },
                        "step": "after"
                    }
                },
                "after": {
                    "bos": [],
                    "control": {
                        "transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/configuration/empty_proposal_after_decision.json"
                        }, "step": "execute"}
                }

            }
        },
        {
            "url": base_url + "/api/v1/node/proposal/insured/execute-node", "data":
            {
                "before": {
                    "bos": [],
                    "control": {
                        "transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/configuration/empty_proposal_before_decision.json"
                        },
                        "step": "execute"
                    }
                },
                "execute": {
                    "bos": [
                        {
                            "before_transformer": {
                                "type": "JOLT",
                                "resource_file_path": "specs/configuration/proposal_insured.json"
                            },
                            "binterface": "proposal",
                            "path": "/v1/",
                            "path_variable": "",
                            "role": "output",
                            "name": "proposals",
                            "method": "PUT"
                        }
                    ],
                    "control": {
                        "transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/configuration/empty_proposal_before_decision.json"
                        },
                        "step": "execute"
                    }
                },
                "after": {
                    "bos": [],
                    "control": {
                        "transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/configuration/empty_proposal_after_decision.json"
                        },
                        "step": "execute"
                    }}
            }
        },
        {
            "url": base_url + "/api/v1/node/proposal-plan/create/before", "data":
            {
                "bos": [
                    {
                        "before_transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/configuration/sellable_plan_id.json"
                        },
                        "binterface": "sellable_plan",
                        "path": "/acko/v1/",
                        "path_variable": "",
                        "filters": {},
                        "role": "input",
                        "name": "sellable_plan",
                        "method": "GET"
                    }
                ],
                "control": {
                    "step": "execute"
                }
            }
        },
        {
            "url": base_url + "/api/v1/node/proposal-plan/create/execute", "data":
            {
                "bos": [
                    {
                        "before_transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/configuration/proposal_plan.json"
                        },
                        "binterface": "proposal",
                        "path": "/v1/",
                        "path_variable": "",
                        "role": "output",
                        "name": "proposals",
                        "method": "PUT"
                    }
                ],
                "control": {
                    "step": "execute"
                }
            }
        },
        {
            "url": base_url + "/api/v1/node/proposal-plan/create/after", "data":
            {
                "bos": [

                ],
                "control": {
                    "value": "successful",
                    "step": "execute"
                }
            }
        },
        {
            "url": base_url + "/api/v1/node/pricing/get", "data":
            {
                "before": {},
                "execute": {
                    "bos": [
                        {
                            "input_transform": [
                                {
                                    "operation": "default",
                                    "spec": {
                                        "rule_id": "sureos_retail_pricing_grid_id_1",
                                        "plan_id": "retail_plan_id_for_any_base_plan_or_topup",
                                        "parameters_id": "retail_plan_param_id_for_any_base_plan_or_topup",
                                        "insured_details": [
                                            {
                                                "id": "1234",
                                                "parameters": {
                                                    "age": 34,
                                                    "user_type": "primary"
                                                }
                                            },
                                            {
                                                "id": "12345",
                                                "parameters": {
                                                    "age": 9,
                                                    "user_type": "dependent"
                                                }
                                            },
                                            {
                                                "id": "12345",
                                                "parameters": {
                                                    "age": 65,
                                                    "user_type": "additional_life"
                                                }
                                            }
                                        ],
                                        "pricing_parameters": {
                                            "zone": 1,
                                            "deductible": 0,
                                            "sum_insured": "1000000",
                                            "family_type": "1A1C",
                                            "addons": [
                                                "doctor_on_call",
                                                "waiver_of_30_days_waiting_period",
                                                "inflaction_protect",
                                                "reduction_in_specific_illness_waiting_period",
                                                "all_hands_necessary_hospitilization",
                                                "waiver_of_non_payable_medical_expenses",
                                                "restore_si",
                                                "health_checkup"
                                            ]
                                        }
                                    }
                                },
                                {
                                    "operation": "remove",
                                    "spec": {
                                        "udb": ""
                                    }
                                }
                            ],
                            "host": "https://pricing-service-uat.ackosureosuat.com",
                            "binterface": "pricing",
                            "path": "/pricing-service/v1/",
                            "path_variable": "/calculate",
                            "role": "input",
                            "method": "POST",
                            "name": "pricing",
                            "filter": [],
                            "output_transform": [
                                {
                                    "operation": "shift",
                                    "spec": {
                                        "response": "prospect.response"
                                    }
                                }
                            ]
                        }
                    ]
                },
                "after": {}
            }

        },
        {
            "url": base_url + "/api/v1/node/quote/get", "data":
            {
                "before": {},
                "execute": {
                    "bos": [
                        {
                            "input_transform": [
                                {
                                    "operation": "default",
                                    "spec": {}
                                }
                            ],
                            "host": base_url,
                            "binterface": "quote",
                            "path": "/api/v1/health/",
                            "path_variable": "",
                            "role": "input",
                            "method": "POST",
                            "name": "quote",
                            "filter": [],
                            "headers": {
                                "directory-location": "/acko/health/design"
                            },
                            "output_transform": [
                                {
                                    "operation": "shift",
                                    "spec": {
                                        "quotes": "prospect.quote_details.quotes"
                                    }
                                }
                            ]
                        }
                    ]
                },
                "after": {}
            }
        },
        {
            "url": base_url + "/api/v1/health/orders/execute", "data":
            {
                "execute": {
                    "bos": [
                        {
                            "binterface": "quote-service",
                            "path": "/api/v1/quotes",
                            "http_method": "GET",
                            "path_variables": {
                                "udbId": "health_user_18"
                            },
                            "query_params": {},
                            "input_transformer_file_path": "",
                            "output_transformer_file_path": ""
                        },
                        {
                            "binterface": "order-service",
                            "path": "/api/v1/orders",
                            "http_method": "POST",
                            "path_variables": {},
                            "query_params": {},
                            "input_transformer_file_path": "",
                            "output_transformer_file_path": "specs/order_output_transform_final.json"
                        }
                    ]
                },
                "after": {
                    "control": [
                        {
                            "value": "success",
                            "decision": "payment_plan_node"
                        }
                    ]
                }
            }
        },
        {
            "url": base_url + "/api/v1/health/orders/paymentplan/execute", "data":
            {
                "execute": {
                    "bos": [
                        {
                            "binterface": "central-payment-service",
                            "path": "/api/v1/payment-plans/{paymentPlanId}",
                            "http_method": "POST",
                            "path_variables": {
                            },
                            "configuration": "specs/configuration/schedules_configuration.json",
                            "query_params": {},
                            "output_transformer_file_path": "specs/payment_output_transform.json"
                        },
                        {
                            "binterface": "central-payment-service",
                            "path": "api/v1/generate-plan-id",
                            "http_method": "POST",
                            "path_variables": {
                            },
                            "query_params": {}
                        },
                        {
                            "binterface": "central-payment-service",
                            "path": "/api/v1/internal/payment-plans/{paymentPlanId}/payments",
                            "http_method": "POST",
                            "path_variables": {
                            },
                            "query_params": {}
                        }
                    ]
                }
            }
        },
        {
            "url": base_url + "/api/v1/fulfill/order/before", "data":
            {
                "bos": [
                    {
                        "name": "order_fulfillment_preprocessor",
                        "binterface": "OrderFulfillmentPreProcessor",
                        "path": "acko/v1/",
                        "role": "input",
                        "method": "GET",
                        "path_variable": "arav_1",
                        "before_transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/fulfillment_order.json"
                        }
                    }
                ],
                "control": {
                    "value": ".*",
                    "step": "execute"
                }
            }
        },
        {
            "url": base_url + "/api/v1/fulfill/order/execute", "data":
            {

                "bos": [
                    {
                        "name": "order_fulfillment_evaluator",
                        "binterface": "OrderFulfillmentEvaluator",
                        "path": "acko/v1/",
                        "role": "input",
                        "method": "POST",
                        "before_transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/fulfillment_order_evaluator.json"
                        }
                    }
                ],
                "control": {
                    "key": "kyc_status",
                    "value": "success",
                    "step": "policy"
                },
                "result": {
                    "proposal_status": "locked",
                    "kyc_header": {
                        "kyc_status": "SUCCESS"
                    }
                }
            }

        },
        # {
        #     "url": base_url + "/api/v1/node/proposal/order/execute", "data":
        #     {
        #         "bos": [
        #             {
        #                 "before_transformer": {
        #                     "type": "JOLT",
        #                     "resource_file_path": "specs/configuration/proposal_order.json"
        #                 },
        #                 "binterface": "proposal",
        #                 "path": "/v1/",
        #                 "path_variable": "",
        #                 "role": "output",
        #                 "name": "proposals",
        #                 "method": "PUT"
        #             }
        #         ],
        #     }
        # },
        {
            "url": base_url + "/api/v1/node/proposal/premium/execute", "data":
            {
                "bos": [
                    {
                        "before_transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/configuration/proposal_premium.json"
                        },
                        "binterface": "proposal",
                        "path": "/v1/",
                        "path_variable": "",
                        "role": "output",
                        "name": "proposals",
                        "method": "PUT"
                    }
                ],
            }
        },
        {
            "url": base_url + "/api/v1/node/proposal/lock/execute", "data":
            {
                "bos": [
                    {
                        "binterface": "proposal",
                        "path": "/v1/",
                        "path_variable": "",
                        "role": "output",
                        "name": "proposals",
                        "method": "LOCK"
                    }
                ],
            }
        },
        {
            "url": base_url + "/api/v1/health/policy/validate-proposal", "data":
            {
                "bos": [
                    {
                        "before_transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/configuration/proposal_validate.json"
                        },
                        "binterface": "validate-proposal",
                        "path": "/api/v1/health/policy",
                        "filters": {
                            "directory_location": "/acko/health/design"
                        },
                        "name": "proposal_validation",
                        "method": "POST"
                    }
                ],
                "control": {
                    "decision": "true",
                    "step": "execute"
                }
            }
        },
        {
            "url": base_url + "/api/v1/health/policy/create", "data":
            {
                "bos": [
                    {
                        "before_transformer": {
                            "type": "JOLT",
                            "resource_file_path": "specs/configuration/proposal_validate.json"
                        },
                        "binterface": "validate-proposal",
                        "path": "/api/v1/health/policy",
                        "filters": {
                            "directory_location": "/acko/health/design"
                        },
                        "name": "proposal_validation",
                        "method": "POST"
                    }
                ],
                "control": {
                    "decision": "true",
                    "step": "execute"
                }
            }
        }

    ]

    # Iterate over each API endpoint
    for endpoint in api_endpoints:
        # Add input data from the previous response, if any
        if mega_json:
            endpoint["data"]["result"] = mega_json

        # Send POST request to the API endpoint
        print("url - " + endpoint["url"])
        print(json.dumps(endpoint["data"]))

        response = hit_rest_api(endpoint["url"], endpoint["data"], "POST")

        # If response is received, update input data for the next call
        if response:
            mega_json = response
        print(f"Response from {endpoint['url']}: {json.dumps(response)}")

        # UPDATE back to UDB
        response = hit_rest_api(
            "https://sureos-input-data-capture.ackosureosuat.com/acko/v1/input-data-capture/" + udb_id,
            {
                "input_data_id": udb_id,
                "input_data": mega_json
            }, "PUT")

        print("MJ Updated\n")


if __name__ == "__main__":
    main()
