test_relation_model_label_config="""<View>
    <Header value="Use create relation icon or shortcut 'r' to create relation between chunks"/>
    <Relations>
    <Relation value="0" model="re_redl_bodypart_problem_biobert"/>
    <Relation value="1" model="re_redl_bodypart_problem_biobert"/>
    </Relations>
    <Labels name="label" toName="text">
    <Label value="Injury_or_Poisoning" model="ner_jsl" background="#e6a59e"/>
    <Label value="Direction" model="ner_jsl" background="#0e2fdb"/>
    <Label value="Test" model="ner_jsl" background="#1c05e7"/>
    <Label value="Admission_Discharge" model="ner_jsl" background="#942420"/>
    <Label value="Death_Entity" model="ner_jsl" background="#5efcf1"/>
    <Label value="Relationship_Status" model="ner_jsl" background="#8085ba"/>
    <Label value="Duration" model="ner_jsl" background="#ca5fe5"/>
    <Label value="Respiration" model="ner_jsl" background="#13e130"/>
    <Label value="Hyperlipidemia" model="ner_jsl" background="#6ff386"/>
    <Label value="Birth_Entity" model="ner_jsl" background="#587bbd"/>
    <Label value="Age" model="ner_jsl" background="#3417a1"/>
    <Label value="Labour_Delivery" model="ner_jsl" background="#9f0dc8"/>
    <Label value="Family_History_Header" model="ner_jsl" background="#c53084"/>
    <Label value="BMI" model="ner_jsl" background="#9f3dcc"/>
    <Label value="Temperature" model="ner_jsl" background="#c7285c"/>
    <Label value="Alcohol" model="ner_jsl" background="#91d781"/>
    <Label value="Kidney_Disease" model="ner_jsl" background="#c2c3fe"/>
    <Label value="Oncological" model="ner_jsl" background="#ecb35c"/>
    <Label value="Medical_History_Header" model="ner_jsl" background="#89a3c8"/>
    <Label value="Cerebrovascular_Disease" model="ner_jsl" background="#d40ece"/>
    <Label value="Oxygen_Therapy" model="ner_jsl" background="#fcb356"/>
    <Label value="O2_Saturation" model="ner_jsl" background="#7b5f60"/>
    <Label value="Psychological_Condition" model="ner_jsl" background="#9c8a47"/>
    <Label value="Heart_Disease" model="ner_jsl" background="#34d295"/>
    <Label value="Employment" model="ner_jsl" background="#7c3a45"/>
    <Label value="Obesity" model="ner_jsl" background="#e690a6"/>
    <Label value="Disease_Syndrome_Disorder" model="ner_jsl" background="#abc181"/>
    <Label value="Pregnancy" model="ner_jsl" background="#5e10e1"/>
    <Label value="ImagingFindings" model="ner_jsl" background="#d1eae3"/>
    <Label value="Procedure" model="ner_jsl" background="#599f6b"/>
    <Label value="Medical_Device" model="ner_jsl" background="#ad73bf"/>
    <Label value="Race_Ethnicity" model="ner_jsl" background="#975326"/>
    <Label value="Section_Header" model="ner_jsl" background="#ee38cc"/>
    <Label value="Symptom" model="ner_jsl" background="#c00676"/>
    <Label value="Treatment" model="ner_jsl" background="#55c988"/>
    <Label value="Substance" model="ner_jsl" background="#9a145b"/>
    <Label value="Route" model="ner_jsl" background="#abbbbc"/>
    <Label value="Drug_Ingredient" model="ner_jsl" background="#e540e2"/>
    <Label value="Blood_Pressure" model="ner_jsl" background="#ece6f8"/>
    <Label value="Diet" model="ner_jsl" background="#54445a"/>
    <Label value="External_body_part_or_region" model="ner_jsl" background="#53171f"/>
    <Label value="LDL" model="ner_jsl" background="#c28b34"/>
    <Label value="VS_Finding" model="ner_jsl" background="#4a55bf"/>
    <Label value="Allergen" model="ner_jsl" background="#4ebc07"/>
    <Label value="EKG_Findings" model="ner_jsl" background="#bad0f8"/>
    <Label value="Imaging_Technique" model="ner_jsl" background="#6901ea"/>
    <Label value="Triglycerides" model="ner_jsl" background="#498f86"/>
    <Label value="RelativeTime" model="ner_jsl" background="#b03c48"/>
    <Label value="Gender" model="ner_jsl" background="#e70749"/>
    <Label value="Pulse" model="ner_jsl" background="#705f61"/>
    <Label value="Social_History_Header" model="ner_jsl" background="#37678d"/>
    <Label value="Substance_Quantity" model="ner_jsl" background="#0713fe"/>
    <Label value="Diabetes" model="ner_jsl" background="#10d936"/>
    <Label value="Modifier" model="ner_jsl" background="#3a7cc2"/>
    <Label value="Internal_organ_or_component" model="ner_jsl" background="#07c074"/>
    <Label value="Clinical_Dept" model="ner_jsl" background="#e4a844"/>
    <Label value="Form" model="ner_jsl" background="#0ff8a9"/>
    <Label value="Drug_BrandName" model="ner_jsl" background="#e9b677"/>
    <Label value="Strength" model="ner_jsl" background="#0038d5"/>
    <Label value="Fetus_NewBorn" model="ner_jsl" background="#9e3796"/>
    <Label value="RelativeDate" model="ner_jsl" background="#f586c5"/>
    <Label value="Height" model="ner_jsl" background="#c4884e"/>
    <Label value="Test_Result" model="ner_jsl" background="#91a6b6"/>
    <Label value="Sexually_Active_or_Sexual_Orientation" model="ner_jsl" background="#8dbb63"/>
    <Label value="Frequency" model="ner_jsl" background="#474956"/>
    <Label value="Time" model="ner_jsl" background="#c20bdb"/>
    <Label value="Weight" model="ner_jsl" background="#82737d"/>
    <Label value="Vaccine" model="ner_jsl" background="#eba756"/>
    <Label value="Vital_Signs_Header" model="ner_jsl" background="#495e35"/>
    <Label value="Communicable_Disease" model="ner_jsl" background="#b83d15"/>
    <Label value="Dosage" model="ner_jsl" background="#42a0cd"/>
    <Label value="Overweight" model="ner_jsl" background="#44ff8f"/>
    <Label value="Hypertension" model="ner_jsl" background="#a6f804"/>
    <Label value="HDL" model="ner_jsl" background="#4eccd3"/>
    <Label value="Total_Cholesterol" model="ner_jsl" background="#e70acf"/>
    <Label value="Smoking" model="ner_jsl" background="#d8db39"/>
    <Label value="Date" model="ner_jsl" background="#55b9e1"/>
    </Labels>
    <Text name="text" value="$text"/>
    </View>
"""
ner_dl_label_config="""<View>
      <Labels name="label" toName="text">
        <Label value="PER" model="ner_dl" background="#234d2a"/>
        <Label value="LOC" model="ner_dl" background="#5c94ac"/>
        <Label value="ORG" model="ner_dl" background="#f59fb8"/>
        <Label value="MISC" model="ner_dl" background="#4cf3b9"/>
      </Labels>
      <Text name="text" value="$text"/>
    </View>
"""
ner_dl_interface_preview_xpath=(
    "//div[@id='editor-wrap' and "
    ".//span[@class='ant-tag' and text()='PER'] and "
    ".//span[@class='ant-tag' and text()='LOC'] and "
    ".//span[@class='ant-tag' and text()='ORG'] and "
    ".//span[@class='ant-tag' and text()='MISC']]"
)
test_assertion_training_label_config="""<View>
        <Labels name="ner" toName="text">
        <Label value="Imaging_Technique" background="red"/>
        <Label value="Vaccine" background="green" hotkey="_"/>
        <Label value="Allergen" background=" green " hotkey="_"/>
        <Label value="Treatment" background="green" hotkey="_"/>
        <Label value="Diet" background="green" hotkey="_"/>
        <Label value="Clinical_Dept" background="green" hotkey="_"/>
        <Label value="Medical_Device" background="green" hotkey="_"/>
        <Label value="Admission_Discharge" background="green" hotkey="_"/>
        <Label value="Pregnancy_Delivery_Puerperium" background="pink" hotkey="_"/>
        <Label value="Pregnancy" background="pink" hotkey="_"/>
        <Label value="Labour_Delivery" background="pink" hotkey="_"/>
        <Label value="Puerperium" background="pink" hotkey="_"/>
        <Label value="Fetus_NewBorn" background="pink" hotkey="_"/>
        <Label value="Oncological" background="pink" hotkey="_"/>
        <Label value="Communicable_Disease" background="pink" hotkey="_"/>
        <Label value="Psychological_Condition" background="pink" hotkey="_"/>
        <Label value="Injury_or_Poisoning" background="pink" hotkey="_"/>
        <Label value="Disease_Syndrome_Disorder" background="pink" hotkey="4"/>
        <Label value="Symptom" background="blue" hotkey="3"/>
        <Label value="Assertion_DOBirth" background="red" hotkey="_"/>
        <Label value="Assertion_DODeath" background="red" hotkey="_"/>
        <Label value="Birth_Entity" background="brown" hotkey="0"/>
        <Label value="Death_Entity" background="brown" hotkey="9"/>
        <Label value="Age" background="brown" hotkey="1"/>
        <Label value="Gender" background="gray" hotkey="2"/>
        <Label value="Female_Reproductive_Status" background="gray" hotkey="_"/>
        <Label value="Race_Ethnicity" background="gray" hotkey="_"/>
        <Label value="Employment" background="brown" hotkey="_"/>
        <Label value="Relationship_Status" background="brown" hotkey="_"/>
        <Label value="Sexually_Active_or_Sexual_Orientation" background="brown" hotkey="_"/>
        <Label value="Temperature" background="olive" hotkey="_"/>
        <Label value="Pulse" background="gold" hotkey="_"/>
        <Label value="Respiration" background="tan" hotkey="_"/>
        <Label value="Blood_Pressure" background="brown" hotkey="_"/>
        <Label value="O2_Saturation" background="orange" hotkey="_"/>
        <Label value="VS_Finding" background="orange" hotkey="_"/>
        <Label value="Oxygen_Therapy" background="orange" hotkey="_"/>
        <Label value="Weight" background="tan" hotkey="_"/>
        <Label value="Height" background="tan" hotkey="_"/>
        <Label value="BMI" background="tan" hotkey="_"/>
        <Label value="External_body_part_or_region" background="orange" hotkey="Q"/>
        <Label value="Internal_organ_or_component" background="orange" hotkey="W"/>
        <Label value="Direction" background="orange" hotkey="E"/>
        <Label value="Smoking" background="gray" hotkey="6"/>
        <Label value="Assertion_SecondHand" background="red" hotkey="_"/>
        <Label value="Alcohol" background="gray" hotkey="7"/>
        <Label value="Assertion_SocialDrinking" background="red" hotkey="_"/>
        <Label value="Substance" background="gray" hotkey="_"/>
        <Label value="Substance_Quantity" background="gray" hotkey="_"/>
        <Label value="Drug_Ingredient" background="gold" hotkey="T"/>
        <Label value="Drug_BrandName" background="green" hotkey="Y"/>
        <Label value="Dosage" background="chocolate" />
        <Label value="Route" background=" chocolate " hotkey="O"/>
        <Label value="Strength" background=" chocolate " hotkey="P"/>
        <Label value="Form" background=" chocolate " hotkey="I"/>
        <Label value="Duration" background="chocolate" hotkey="G"/>
        <Label value="Frequency" background=" chocolate " />
        <Label value="Date" background="blue" hotkey="_"/>
        <Label value="RelativeDate" background="blue" hotkey="F"/>
        <Label value="Time" background="blue" hotkey="_"/>
        <Label value="RelativeTime" background="blue" hotkey="_"/>
        <Label value="Diabetes" background="orange" hotkey="_"/>
        <Label value="Hypertension" background="orange" hotkey="_"/>
        <Label value="Hyperlipidemia" background="orange" hotkey="_"/>
        <Label value="Overweight" background="orange" hotkey="_"/>
        <Label value="Obesity" background="orange" hotkey="_"/>
        <Label value="Kidney_Disease" background="orange" hotkey="_"/>
        <Label value="Heart_Disease" background="orange" hotkey="_"/>
        <Label value="Cerebrovascular_Disease" background="orange" hotkey="_"/>
        <Label value="Modifier" background="olive" hotkey="5"/>
        <Label value="Procedure" background="green" hotkey="8"/>
        <Label value="Test" background="green" hotkey="A"/>
        <Label value="Test_Result" background="orange" hotkey="S"/>
        <Label value="Total_Cholesterol" background="gold" hotkey="_"/>
        <Label value="LDL" background="gold" hotkey="_"/>
        <Label value="HDL" background="gold" hotkey="_"/>
        <Label value="Triglycerides" background="gold" hotkey="_"/>
        <Label value="ImagingFindings" background="orange" hotkey="_"/>
        <Label value="EKG_Findings" background="orange" hotkey="_"/>
        <Label value="Section_Header" background="gold" hotkey="_"/>
        <Label value="Medical_History_Header" background="green" hotkey="_"/>
        <Label value="Family_History_Header" background="green" hotkey="J"/>
        <Label value="Social_History_Header" background="green" hotkey="K"/>
        <Label value="Vital_Signs_Header" background="green" hotkey="L"/>
        <Label value="Absent" assertion="true" background="red" hotkey="Z"/>
        <Label value="Past" assertion="true" background="red" hotkey="X"/>
        <Label value="Hypothetical" assertion="true" background="red" hotkey="C"/>
        <Label value="Family" assertion="true" background="red" hotkey="V"/>
        <Label value="SomeoneElse" assertion="true" background="red" />
        <Label value="Possible" assertion="true" background="red" hotkey="N"/>
        <Label value="Planned" assertion="true" background="red" hotkey="B"/>
        <Label value="ManualFix" assertion="true" background="blue" hotkey="D"/>
        <Label value="Review" assertion="true" background="blue" hotkey="_"/>
        <Label value="NotInTaxonomy" assertion="true" background="blue" hotkey="_"/>
    </Labels>
    <View style="height: 250px; overflow: auto;">
        <Text name="text" value="$text"/>
    </View>
    </View>
"""
test_incompatible_config_with_spark_nlp_label_config="""<View>
      <Image name="image" value="$image"/>
      <RectangleLabels name="label" toName="image">
        <Label value="Airplane" background="green"/>
        <Label value="Car" background="blue"/>
      </RectangleLabels>
    </View>
"""
test_assertion_model_in_models_hub_label_config="""<View>
  <Labels name="label" toName="text">
    <Label value="Injury_or_Poisoning" model="ner_jsl" background="#9eb32a"/>
    <Label value="Direction" model="ner_jsl" background="#4e71cb"/>
    <Label value="Test" model="ner_jsl" background="#8e5978"/>
    <Label value="Admission_Discharge" model="ner_jsl" background="#9eb99c"/>
    <Label value="Death_Entity" model="ner_jsl" background="#060034"/>
    <Label value="Relationship_Status" model="ner_jsl" background="#f67c45"/>
    <Label value="Duration" model="ner_jsl" background="#ab5404"/>
    <Label value="Respiration" model="ner_jsl" background="#f11a74"/>
    <Label value="Hyperlipidemia" model="ner_jsl" background="#3a9138"/>
    <Label value="Birth_Entity" model="ner_jsl" background="#ef6925"/>
    <Label value="Age" model="ner_jsl" background="#721868"/>
    <Label value="Labour_Delivery" model="ner_jsl" background="#156bf6"/>
    <Label value="Family_History_Header" model="ner_jsl" background="#51c180"/>
    <Label value="BMI" model="ner_jsl" background="#c305f0"/>
    <Label value="Temperature" model="ner_jsl" background="#5828c3"/>
    <Label value="Alcohol" model="ner_jsl" background="#a23cfd"/>
    <Label value="Kidney_Disease" model="ner_jsl" background="#b3be53"/>
    <Label value="Oncological" model="ner_jsl" background="#58ecfe"/>
    <Label value="Medical_History_Header" model="ner_jsl" background="#629566"/>
    <Label value="Cerebrovascular_Disease" model="ner_jsl" background="#a6e064"/>
    <Label value="Oxygen_Therapy" model="ner_jsl" background="#2500fb"/>
    <Label value="O2_Saturation" model="ner_jsl" background="#d3f0f9"/>
    <Label value="Psychological_Condition" model="ner_jsl" background="#a6798f"/>
    <Label value="Heart_Disease" model="ner_jsl" background="#1fcc56"/>
    <Label value="Employment" model="ner_jsl" background="#cf96d6"/>
    <Label value="Obesity" model="ner_jsl" background="#582130"/>
    <Label value="Disease_Syndrome_Disorder" model="ner_jsl" background="#0ac553"/>
    <Label value="Pregnancy" model="ner_jsl" background="#824fd1"/>
    <Label value="ImagingFindings" model="ner_jsl" background="#dddb25"/>
    <Label value="Procedure" model="ner_jsl" background="#c4193a"/>
    <Label value="Medical_Device" model="ner_jsl" background="#703f26"/>
    <Label value="Race_Ethnicity" model="ner_jsl" background="#7a910d"/>
    <Label value="Section_Header" model="ner_jsl" background="#c06bb2"/>
    <Label value="Symptom" model="ner_jsl" background="#62bed3"/>
    <Label value="Treatment" model="ner_jsl" background="#671a13"/>
    <Label value="Substance" model="ner_jsl" background="#47a8ae"/>
    <Label value="Route" model="ner_jsl" background="#d82d27"/>
    <Label value="Drug_Ingredient" model="ner_jsl" background="#f8df63"/>
    <Label value="Blood_Pressure" model="ner_jsl" background="#be6a48"/>
    <Label value="Diet" model="ner_jsl" background="#40511d"/>
    <Label value="External_body_part_or_region" model="ner_jsl" background="#c8284d"/>
    <Label value="LDL" model="ner_jsl" background="#d9d22f"/>
    <Label value="VS_Finding" model="ner_jsl" background="#d082f2"/>
    <Label value="Allergen" model="ner_jsl" background="#f67297"/>
    <Label value="EKG_Findings" model="ner_jsl" background="#05787e"/>
    <Label value="Imaging_Technique" model="ner_jsl" background="#3f5d89"/>
    <Label value="Triglycerides" model="ner_jsl" background="#fc927a"/>
    <Label value="RelativeTime" model="ner_jsl" background="#4d0da6"/>
    <Label value="Gender" model="ner_jsl" background="#a49fc5"/>
    <Label value="Pulse" model="ner_jsl" background="#ceb96d"/>
    <Label value="Social_History_Header" model="ner_jsl" background="#95c6ab"/>
    <Label value="Substance_Quantity" model="ner_jsl" background="#b41345"/>
    <Label value="Diabetes" model="ner_jsl" background="#18322e"/>
    <Label value="Modifier" model="ner_jsl" background="#bb6f21"/>
    <Label value="Internal_organ_or_component" model="ner_jsl" background="#beec05"/>
    <Label value="Clinical_Dept" model="ner_jsl" background="#b8d05e"/>
    <Label value="Form" model="ner_jsl" background="#c14fee"/>
    <Label value="Drug_BrandName" model="ner_jsl" background="#c1323e"/>
    <Label value="Strength" model="ner_jsl" background="#ee21ec"/>
    <Label value="Fetus_NewBorn" model="ner_jsl" background="#a7b670"/>
    <Label value="RelativeDate" model="ner_jsl" background="#268074"/>
    <Label value="Height" model="ner_jsl" background="#a17823"/>
    <Label value="Test_Result" model="ner_jsl" background="#cc56a7"/>
    <Label value="Sexually_Active_or_Sexual_Orientation" model="ner_jsl" background="#ccdaa8"/>
    <Label value="Frequency" model="ner_jsl" background="#02fa14"/>
    <Label value="Time" model="ner_jsl" background="#15f68b"/>
    <Label value="Weight" model="ner_jsl" background="#98218c"/>
    <Label value="Vaccine" model="ner_jsl" background="#82ee9f"/>
    <Label value="Vital_Signs_Header" model="ner_jsl" background="#72e61c"/>
    <Label value="Communicable_Disease" model="ner_jsl" background="#ff84ed"/>
    <Label value="Dosage" model="ner_jsl" background="#5d146f"/>
    <Label value="Overweight" model="ner_jsl" background="#a79c13"/>
    <Label value="Hypertension" model="ner_jsl" background="#be4469"/>
    <Label value="HDL" model="ner_jsl" background="#c65cc6"/>
    <Label value="Total_Cholesterol" model="ner_jsl" background="#375b92"/>
    <Label value="Smoking" model="ner_jsl" background="#c39701"/>
    <Label value="Date" model="ner_jsl" background="#0d4fcd"/>
    <Label value="Present" model="assertion_jsl" background="#c4f57e" assertion="true"/>
    <Label value="Absent" model="assertion_jsl" background="#7ea48f" assertion="true"/>
    <Label value="Possible" model="assertion_jsl" background="#cfff64" assertion="true"/>
    <Label value="Planned" model="assertion_jsl" background="#f4b81b" assertion="true"/>
    <Label value="Someoneelse" model="assertion_jsl" background="#23167e" assertion="true"/>
    <Label value="Past" model="assertion_jsl" background="#44caaa" assertion="true"/>
    <Label value="Family" model="assertion_jsl" background="#421430" assertion="true"/>
    <Label value="None" model="assertion_jsl" background="#2979ee" assertion="true"/>
    <Label value="Hypotetical" model="assertion_jsl" background="#238c9c" assertion="true"/>
  </Labels>
  <Text name="text" value="$text"/>
</View>
"""
assertion_jsl_labels = ["Present", "Absent", "Possible", "Someoneelse", "Past", "Family", "None", "Hypotetical"]
test_ner_and_classification_model_label_config="""<View>
  <Text name="text" value="$text"/>
  <Labels name="label" toName="text">
    <Label value="Test_Result" model="ner_jsl_ner_wip_greedy_biobert" background="#490de5"/>
    <Label value="Relationship_Status" model="ner_jsl_ner_wip_greedy_biobert" background="#ea41dd"/>
    <Label value="RelativeDate" model="ner_jsl_ner_wip_greedy_biobert" background="#51489f"/>
    <Label value="Blood_Pressure" model="ner_jsl_ner_wip_greedy_biobert" background="#db70dd"/>
    <Label value="Triglycerides" model="ner_jsl_ner_wip_greedy_biobert" background="#7f342b"/>
    <Label value="Smoking" model="ner_jsl_ner_wip_greedy_biobert" background="#baec09"/>
    <Label value="Pregnancy" model="ner_jsl_ner_wip_greedy_biobert" background="#319905"/>
    <Label value="Medical_History_Header" model="ner_jsl_ner_wip_greedy_biobert" background="#6ddb59"/>
    <Label value="LDL" model="ner_jsl_ner_wip_greedy_biobert" background="#94ff8a"/>
    <Label value="Hypertension" model="ner_jsl_ner_wip_greedy_biobert" background="#4c2fcf"/>
    <Label value="Hyperlipidemia" model="ner_jsl_ner_wip_greedy_biobert" background="#67c1e9"/>
    <Label value="Frequency" model="ner_jsl_ner_wip_greedy_biobert" background="#257ecf"/>
    <Label value="BMI" model="ner_jsl_ner_wip_greedy_biobert" background="#ef6eac"/>
    <Label value="Internal_organ_or_component" model="ner_jsl_ner_wip_greedy_biobert" background="#cb60c5"/>
    <Label value="Allergen" model="ner_jsl_ner_wip_greedy_biobert" background="#ea5a50"/>
    <Label value="Fetus_NewBorn" model="ner_jsl_ner_wip_greedy_biobert" background="#d47fb5"/>
    <Label value="Substance_Quantity" model="ner_jsl_ner_wip_greedy_biobert" background="#e1ef02"/>
    <Label value="Time" model="ner_jsl_ner_wip_greedy_biobert" background="#e411ae"/>
    <Label value="Temperature" model="ner_jsl_ner_wip_greedy_biobert" background="#3e0016"/>
    <Label value="Procedure" model="ner_jsl_ner_wip_greedy_biobert" background="#738318"/>
    <Label value="Strength" model="ner_jsl_ner_wip_greedy_biobert" background="#873981"/>
    <Label value="Treatment" model="ner_jsl_ner_wip_greedy_biobert" background="#1b5019"/>
    <Label value="HDL" model="ner_jsl_ner_wip_greedy_biobert" background="#aad917"/>
    <Label value="Alcohol" model="ner_jsl_ner_wip_greedy_biobert" background="#b4ba57"/>
    <Label value="Birth_Entity" model="ner_jsl_ner_wip_greedy_biobert" background="#f34f94"/>
    <Label value="Diet" model="ner_jsl_ner_wip_greedy_biobert" background="#29b902"/>
    <Label value="Weight" model="ner_jsl_ner_wip_greedy_biobert" background="#031ef1"/>
    <Label value="Oxygen_Therapy" model="ner_jsl_ner_wip_greedy_biobert" background="#27490f"/>
    <Label value="Injury_or_Poisoning" model="ner_jsl_ner_wip_greedy_biobert" background="#55e78e"/>
    <Label value="Section_Header" model="ner_jsl_ner_wip_greedy_biobert" background="#b44532"/>
    <Label value="Obesity" model="ner_jsl_ner_wip_greedy_biobert" background="#e71625"/>
    <Label value="EKG_Findings" model="ner_jsl_ner_wip_greedy_biobert" background="#f32c02"/>
    <Label value="Gender" model="ner_jsl_ner_wip_greedy_biobert" background="#78aae0"/>
    <Label value="Height" model="ner_jsl_ner_wip_greedy_biobert" background="#42301b"/>
    <Label value="Social_History_Header" model="ner_jsl_ner_wip_greedy_biobert" background="#4f5812"/>
    <Label value="Diabetes" model="ner_jsl_ner_wip_greedy_biobert" background="#be9d72"/>
    <Label value="Route" model="ner_jsl_ner_wip_greedy_biobert" background="#6df6ae"/>
    <Label value="Race_Ethnicity" model="ner_jsl_ner_wip_greedy_biobert" background="#9dd855"/>
    <Label value="Substance" model="ner_jsl_ner_wip_greedy_biobert" background="#7f1a3a"/>
    <Label value="Drug" model="ner_jsl_ner_wip_greedy_biobert" background="#6686fc"/>
    <Label value="External_body_part_or_region" model="ner_jsl_ner_wip_greedy_biobert" background="#32033e"/>
    <Label value="RelativeTime" model="ner_jsl_ner_wip_greedy_biobert" background="#b0f09f"/>
    <Label value="Admission_Discharge" model="ner_jsl_ner_wip_greedy_biobert" background="#7fc083"/>
    <Label value="Psychological_Condition" model="ner_jsl_ner_wip_greedy_biobert" background="#76a752"/>
    <Label value="Total_Cholesterol" model="ner_jsl_ner_wip_greedy_biobert" background="#37b2bc"/>
    <Label value="Labour_Delivery" model="ner_jsl_ner_wip_greedy_biobert" background="#3d92fa"/>
    <Label value="Imaging_Technique" model="ner_jsl_ner_wip_greedy_biobert" background="#816966"/>
    <Label value="Date" model="ner_jsl_ner_wip_greedy_biobert" background="#ae8c51"/>
    <Label value="Form" model="ner_jsl_ner_wip_greedy_biobert" background="#9c30a6"/>
    <Label value="Overweight" model="ner_jsl_ner_wip_greedy_biobert" background="#130ca2"/>
    <Label value="Cerebrovascular_Disease" model="ner_jsl_ner_wip_greedy_biobert" background="#cbfff1"/>
    <Label value="Vital_Signs_Header" model="ner_jsl_ner_wip_greedy_biobert" background="#a7185c"/>
    <Label value="Oncological" model="ner_jsl_ner_wip_greedy_biobert" background="#1abc08"/>
    <Label value="ImagingFindings" model="ner_jsl_ner_wip_greedy_biobert" background="#f6a489"/>
    <Label value="Communicable_Disease" model="ner_jsl_ner_wip_greedy_biobert" background="#44fda7"/>
    <Label value="Duration" model="ner_jsl_ner_wip_greedy_biobert" background="#56066d"/>
    <Label value="Vaccine" model="ner_jsl_ner_wip_greedy_biobert" background="#004b38"/>
    <Label value="Kidney_Disease" model="ner_jsl_ner_wip_greedy_biobert" background="#acad49"/>
    <Label value="O2_Saturation" model="ner_jsl_ner_wip_greedy_biobert" background="#91b4df"/>
    <Label value="Heart_Disease" model="ner_jsl_ner_wip_greedy_biobert" background="#6f49fe"/>
    <Label value="Employment" model="ner_jsl_ner_wip_greedy_biobert" background="#731075"/>
    <Label value="Sexually_Active_or_Sexual_Orientation" model="ner_jsl_ner_wip_greedy_biobert" background="#c30c9c"/>
    <Label value="Test" model="ner_jsl_ner_wip_greedy_biobert" background="#166329"/>
    <Label value="Disease_Syndrome_Disorder" model="ner_jsl_ner_wip_greedy_biobert" background="#fa85e9"/>
    <Label value="Respiration" model="ner_jsl_ner_wip_greedy_biobert" background="#bf43f1"/>
    <Label value="Direction" model="ner_jsl_ner_wip_greedy_biobert" background="#0ccd7a"/>
    <Label value="Medical_Device" model="ner_jsl_ner_wip_greedy_biobert" background="#6d3685"/>
    <Label value="Clinical_Dept" model="ner_jsl_ner_wip_greedy_biobert" background="#925e39"/>
    <Label value="Modifier" model="ner_jsl_ner_wip_greedy_biobert" background="#eca753"/>
    <Label value="Symptom" model="ner_jsl_ner_wip_greedy_biobert" background="#744af7"/>
    <Label value="Pulse" model="ner_jsl_ner_wip_greedy_biobert" background="#a9db53"/>
    <Label value="Age" model="ner_jsl_ner_wip_greedy_biobert" background="#366fd3"/>
    <Label value="Death_Entity" model="ner_jsl_ner_wip_greedy_biobert" background="#62a68f"/>
    <Label value="Dosage" model="ner_jsl_ner_wip_greedy_biobert" background="#d7df24"/>
    <Label value="Family_History_Header" model="ner_jsl_ner_wip_greedy_biobert" background="#18b5dd"/>
    <Label value="VS_Finding" model="ner_jsl_ner_wip_greedy_biobert" background="#0bcb21"/>
  </Labels>
  <Choices name="Female" toName="text" choice="single" model="classification_classifierdl_gender_biobert">
    <Choice value="Female"/>
    <Choice value="Male"/>
    <Choice value="Unknown"/>
  </Choices>
</View>
"""
test_ner_classification_and_assertion_model_label_config="""<View>
  <Text name="text" value="$text"/>
  <Labels name="label" toName="text">
    <Label value="Test_Result" model="ner_jsl_ner_wip_greedy_biobert" background="#490de5"/>
    <Label value="Relationship_Status" model="ner_jsl_ner_wip_greedy_biobert" background="#ea41dd"/>
    <Label value="RelativeDate" model="ner_jsl_ner_wip_greedy_biobert" background="#51489f"/>
    <Label value="Blood_Pressure" model="ner_jsl_ner_wip_greedy_biobert" background="#db70dd"/>
    <Label value="Triglycerides" model="ner_jsl_ner_wip_greedy_biobert" background="#7f342b"/>
    <Label value="Smoking" model="ner_jsl_ner_wip_greedy_biobert" background="#baec09"/>
    <Label value="Pregnancy" model="ner_jsl_ner_wip_greedy_biobert" background="#319905"/>
    <Label value="Medical_History_Header" model="ner_jsl_ner_wip_greedy_biobert" background="#6ddb59"/>
    <Label value="LDL" model="ner_jsl_ner_wip_greedy_biobert" background="#94ff8a"/>
    <Label value="Hypertension" model="ner_jsl_ner_wip_greedy_biobert" background="#4c2fcf"/>
    <Label value="Hyperlipidemia" model="ner_jsl_ner_wip_greedy_biobert" background="#67c1e9"/>
    <Label value="Frequency" model="ner_jsl_ner_wip_greedy_biobert" background="#257ecf"/>
    <Label value="BMI" model="ner_jsl_ner_wip_greedy_biobert" background="#ef6eac"/>
    <Label value="Internal_organ_or_component" model="ner_jsl_ner_wip_greedy_biobert" background="#cb60c5"/>
    <Label value="Allergen" model="ner_jsl_ner_wip_greedy_biobert" background="#ea5a50"/>
    <Label value="Fetus_NewBorn" model="ner_jsl_ner_wip_greedy_biobert" background="#d47fb5"/>
    <Label value="Substance_Quantity" model="ner_jsl_ner_wip_greedy_biobert" background="#e1ef02"/>
    <Label value="Time" model="ner_jsl_ner_wip_greedy_biobert" background="#e411ae"/>
    <Label value="Temperature" model="ner_jsl_ner_wip_greedy_biobert" background="#3e0016"/>
    <Label value="Procedure" model="ner_jsl_ner_wip_greedy_biobert" background="#738318"/>
    <Label value="Strength" model="ner_jsl_ner_wip_greedy_biobert" background="#873981"/>
    <Label value="Treatment" model="ner_jsl_ner_wip_greedy_biobert" background="#1b5019"/>
    <Label value="HDL" model="ner_jsl_ner_wip_greedy_biobert" background="#aad917"/>
    <Label value="Alcohol" model="ner_jsl_ner_wip_greedy_biobert" background="#b4ba57"/>
    <Label value="Birth_Entity" model="ner_jsl_ner_wip_greedy_biobert" background="#f34f94"/>
    <Label value="Diet" model="ner_jsl_ner_wip_greedy_biobert" background="#29b902"/>
    <Label value="Weight" model="ner_jsl_ner_wip_greedy_biobert" background="#031ef1"/>
    <Label value="Oxygen_Therapy" model="ner_jsl_ner_wip_greedy_biobert" background="#27490f"/>
    <Label value="Injury_or_Poisoning" model="ner_jsl_ner_wip_greedy_biobert" background="#55e78e"/>
    <Label value="Section_Header" model="ner_jsl_ner_wip_greedy_biobert" background="#b44532"/>
    <Label value="Obesity" model="ner_jsl_ner_wip_greedy_biobert" background="#e71625"/>
    <Label value="EKG_Findings" model="ner_jsl_ner_wip_greedy_biobert" background="#f32c02"/>
    <Label value="Gender" model="ner_jsl_ner_wip_greedy_biobert" background="#78aae0"/>
    <Label value="Height" model="ner_jsl_ner_wip_greedy_biobert" background="#42301b"/>
    <Label value="Social_History_Header" model="ner_jsl_ner_wip_greedy_biobert" background="#4f5812"/>
    <Label value="Diabetes" model="ner_jsl_ner_wip_greedy_biobert" background="#be9d72"/>
    <Label value="Route" model="ner_jsl_ner_wip_greedy_biobert" background="#6df6ae"/>
    <Label value="Race_Ethnicity" model="ner_jsl_ner_wip_greedy_biobert" background="#9dd855"/>
    <Label value="Substance" model="ner_jsl_ner_wip_greedy_biobert" background="#7f1a3a"/>
    <Label value="Drug" model="ner_jsl_ner_wip_greedy_biobert" background="#6686fc"/>
    <Label value="External_body_part_or_region" model="ner_jsl_ner_wip_greedy_biobert" background="#32033e"/>
    <Label value="RelativeTime" model="ner_jsl_ner_wip_greedy_biobert" background="#b0f09f"/>
    <Label value="Admission_Discharge" model="ner_jsl_ner_wip_greedy_biobert" background="#7fc083"/>
    <Label value="Psychological_Condition" model="ner_jsl_ner_wip_greedy_biobert" background="#76a752"/>
    <Label value="Total_Cholesterol" model="ner_jsl_ner_wip_greedy_biobert" background="#37b2bc"/>
    <Label value="Labour_Delivery" model="ner_jsl_ner_wip_greedy_biobert" background="#3d92fa"/>
    <Label value="Imaging_Technique" model="ner_jsl_ner_wip_greedy_biobert" background="#816966"/>
    <Label value="Date" model="ner_jsl_ner_wip_greedy_biobert" background="#ae8c51"/>
    <Label value="Form" model="ner_jsl_ner_wip_greedy_biobert" background="#9c30a6"/>
    <Label value="Overweight" model="ner_jsl_ner_wip_greedy_biobert" background="#130ca2"/>
    <Label value="Cerebrovascular_Disease" model="ner_jsl_ner_wip_greedy_biobert" background="#cbfff1"/>
    <Label value="Vital_Signs_Header" model="ner_jsl_ner_wip_greedy_biobert" background="#a7185c"/>
    <Label value="Oncological" model="ner_jsl_ner_wip_greedy_biobert" background="#1abc08"/>
    <Label value="ImagingFindings" model="ner_jsl_ner_wip_greedy_biobert" background="#f6a489"/>
    <Label value="Communicable_Disease" model="ner_jsl_ner_wip_greedy_biobert" background="#44fda7"/>
    <Label value="Duration" model="ner_jsl_ner_wip_greedy_biobert" background="#56066d"/>
    <Label value="Vaccine" model="ner_jsl_ner_wip_greedy_biobert" background="#004b38"/>
    <Label value="Kidney_Disease" model="ner_jsl_ner_wip_greedy_biobert" background="#acad49"/>
    <Label value="O2_Saturation" model="ner_jsl_ner_wip_greedy_biobert" background="#91b4df"/>
    <Label value="Heart_Disease" model="ner_jsl_ner_wip_greedy_biobert" background="#6f49fe"/>
    <Label value="Employment" model="ner_jsl_ner_wip_greedy_biobert" background="#731075"/>
    <Label value="Sexually_Active_or_Sexual_Orientation" model="ner_jsl_ner_wip_greedy_biobert" background="#c30c9c"/>
    <Label value="Test" model="ner_jsl_ner_wip_greedy_biobert" background="#166329"/>
    <Label value="Disease_Syndrome_Disorder" model="ner_jsl_ner_wip_greedy_biobert" background="#fa85e9"/>
    <Label value="Respiration" model="ner_jsl_ner_wip_greedy_biobert" background="#bf43f1"/>
    <Label value="Direction" model="ner_jsl_ner_wip_greedy_biobert" background="#0ccd7a"/>
    <Label value="Medical_Device" model="ner_jsl_ner_wip_greedy_biobert" background="#6d3685"/>
    <Label value="Clinical_Dept" model="ner_jsl_ner_wip_greedy_biobert" background="#925e39"/>
    <Label value="Modifier" model="ner_jsl_ner_wip_greedy_biobert" background="#eca753"/>
    <Label value="Symptom" model="ner_jsl_ner_wip_greedy_biobert" background="#744af7"/>
    <Label value="Pulse" model="ner_jsl_ner_wip_greedy_biobert" background="#a9db53"/>
    <Label value="Age" model="ner_jsl_ner_wip_greedy_biobert" background="#366fd3"/>
    <Label value="Death_Entity" model="ner_jsl_ner_wip_greedy_biobert" background="#62a68f"/>
    <Label value="Dosage" model="ner_jsl_ner_wip_greedy_biobert" background="#d7df24"/>
    <Label value="Family_History_Header" model="ner_jsl_ner_wip_greedy_biobert" background="#18b5dd"/>
    <Label value="VS_Finding" model="ner_jsl_ner_wip_greedy_biobert" background="#0bcb21"/>
    <Label value="absent" model="assertion_dl_biobert" background="#cfea03" assertion="true"/>
    <Label value="present" model="assertion_dl_biobert" background="#3e3c9f" assertion="true"/>
    <Label value="conditional" model="assertion_dl_biobert" background="#9fc8c8" assertion="true"/>
    <Label value="associated_with_someone_else" model="assertion_dl_biobert" background="#7e8e57" assertion="true"/>
    <Label value="hypothetical" model="assertion_dl_biobert" background="#4347e9" assertion="true"/>
    <Label value="possible" model="assertion_dl_biobert" background="#e1f076" assertion="true"/>
  </Labels>
  <Choices name="Female" toName="text" choice="single" model="classification_classifierdl_gender_biobert">
    <Choice value="Female"/>
    <Choice value="Male"/>
    <Choice value="Unknown"/>
  </Choices>
</View>
"""
assertion_biobert_labels=["absent", "present", "conditional", "associated_with_someone_else", "hypothetical", "possible"]

test_classfication_config = """
    <View>
        <Choices name="{}" toName="text" choice="multiple">
            <View style="display: flex; justify-content: space-between">
              <View style="width: 50%">
                <Header value="Select Topics" />
                <Choice value="Politics"/>
                <Choice value="Business"/>
                <Choice value="Sport"/>
              </View>
              <View>
                <Header value="Select Moods" />
                <Choice value="Cheerful"/>
                <Choice value="Melancholy"/>
                <Choice value="Romantic"/>
              </View>
            </View>
        </Choices>
        <Text name="text" value="$text" />
    </View>
"""


test_default_config = """
    <View>
        <Choices name="sentiment" toName="text" choice="multiple">
            <Header value="Document Type"/>
            <Choice value="Referral"/>
            <Choice value="Operative"/>
            <Choice value="Discharge"/>
            <Choice value="Assessment"/>
            <Choice value="Note"/>
        </Choices>
        <Labels name="label" toName="text">
            <Label value="Person" background="red"/>
            <Label value="Organization" background="darkorange"/>
            <Label value="Fact" background="orange"/>
            <Label value="Money" background="green"/>
            <Label value="Date" background="darkblue"/>
            <Label value="Time" background="blue"/>
            <Label value="Ordinal" background="purple"/>
            <Label value="Percent" background="#842"/>
            <Label value="Product" background="#428"/>
            <Label value="Language" background="#482"/>
            <Label value="Location" background="rgba(0,0,0,0.8)"/>
        </Labels>
        <Text name="text" value="$text"/>
    </View>
"""


test_ner_training_config = """
    <View>
        <Labels name="label" toName="text">
            <Label value="Medicine" background="red"/>
            <Label value="MedicalCondition" background="darkorange"/>
            <Label value="Pathogen" background="orange"/>
        </Labels>
        <Text name="text" value="$text"/>
    </View>
"""

test_visual_ner_config = """
    <View visualNER="true">
        <View visibleWhen="never">
            <Header value="Recognized Text" />
            <TextArea maxSubmissions="1" name="answer" rows="1" toName="image" perRegion="true"/>
        </View>
        <RectangleLabels name="label" toName="image">
            <Label value="Company" background="green"/>
            <Label value="Date" background="blue"/>
            <Label value="Amount" background="red"/>
        </RectangleLabels>
        <Image name="image" value="$image" zoom="true" zoomControl="true"/>
    </View>
"""

free_ner_model_config = """
    <View>
        <Labels name="label" toName="text">
            <Label value="party_size_description"
            model="ner_nerdl_snips_100d" background="#e07e30"/>
            <Label value="sort"
            model="ner_nerdl_snips_100d" background="#e07e30"/>
            <Label value="restaurant_type"
            model="ner_nerdl_snips_100d" background="#e07e30"/>
            <Label value="spatial_relation"
            model="ner_nerdl_snips_100d" background="#e07e30"/>
            <Label value="poi"
            model="ner_nerdl_snips_100d" background="#e07e30"/>
            <Label value="timeRange"
            model="ner_nerdl_snips_100d" background="#e07e30"/>
            <Label value="cuisine"
            model="ner_nerdl_snips_100d" background="#e07e30"/>
        </Labels>
        <Text name="text" value="$text"/>
    </View>
"""

license_ner_model_config = """
        <View>
        <Labels name="label" toName="text">
            <Label value="DATE"
            model="ner_deid_generic_glove" background="#80831b"/>
            <Label value="NAME"
            model="ner_deid_generic_glove" background="#80831b"/>
            <Label value="LOCATION"
            model="ner_deid_generic_glove" background="#80831b"/>
            <Label value="CONTACT"
            model="ner_deid_generic_glove" background="#80831b"/>
        </Labels>
        <Text name="text" value="$text"/>
        </View>
"""

free_classification_model_config = """
    <View>
    <Text name="text" value="$text"/>
    <Choices name="GetWeather" toName="text" choice="single"
    model="classification_classifierdl_use_snips">
        <Choice value="GetWeather"/>
        <Choice value="PlayMusic"/>
        <Choice value="RateBook"/>
        <Choice value="BookRestaurant"/>
    </Choices>
    </View>
"""

license_classification_model_config = """
    <View>
        <Text name="text" value="$text"/>
        <Choices name="CONCLUSIONS" toName="text" choice="single"
        model="classification_classifierdl_pico_biobert">
            <Choice value="CONCLUSIONS"/>
            <Choice value="DESIGN_SETTING"/>
            <Choice value="INTERVENTION"/>
            <Choice value="PARTICIPANTS"/>
            <Choice value="FINDINGS"/>
            <Choice value="MEASUREMENTS"/>
            <Choice value="AIMS"/>
        </Choices>
    </View>
"""

test_visual_ner_config_for_various_images = """
    <View visualNER="true">
      <View visibleWhen="never">
        <Header value="Recognized Text" />
        <TextArea maxSubmissions="1" name="answer" rows="1" toName="image" perRegion="true"/>
      </View>
      <RectangleLabels name="label" toName="image">
        <Label value="Medicine"/>
        <Label value="Disease"/>
        <Label value="Age"/>
        <Label value="Organ"/>
        <Label value="Result"/>
        <Label value="Temperature"/>
        <Label value="Pressure"/>
        <Label value="Pulse"/>
        <Label value="Weight"/>
      </RectangleLabels>
      <Choices name="Diagnosis" toName="image" choice="single">
        <Choice value="Positive"/>
        <Choice value="Negative"/>
        <Choice value="Unknown"/>
      </Choices>
      <Image name="image" value="$image" zoom="true" zoomControl="true"/>
    </View>
"""

test_image_classification_config = """<View>
  <Image name="image" value="$image"/>
  <Choices name="choice" toName="image" showInLine="true">
    <Choice value="Positive" background="blue"/>
    <Choice value="Negative" background="green" />
  </Choices>
</View>
"""