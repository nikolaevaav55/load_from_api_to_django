TEACHERS = 'structure_Teachers'

TEACHERS_MODELS_FIELDS = """
(
    position,
    degrees,
    academic_rank,
    edu_level,
    gen_experience, 
    spec_experience,
    disciplines,
    qualifications,
    train_directions,
    individ,
    qualific_upgrades,
    ranks,
    department,
    direction,
    image_number,
    individ_id,
    add_info_1,
    add_info_2,
    publications,
    interests,
    author,
    date_of_birth,
    phone,
    email,
    web_site, 
    uid,
    teaching_op
)
"""

EDUCATION_THREE_TABLE = 'sveden_EducationThree'

EDUCATION_THREE_FIELDS = """
(   
    edu_code, 
    edu_name,
    edu_level,
    edu_form,
    number_bf,
    number_bff,
    number_br,
    number_brf,
    number_bm,
    number_bmf,
    number_p,
    number_pf,
    number_all,
    update_time,
    update_date
)
"""

EDUCATION_FIVE_TABLE = 'sveden_EducationFive'

EDUCATION_FIVE_FIELDS = """
(   
    edu_code,
    edu_name,
    edu_level,
    edu_form,
    number_out_perevod,
    number_to_perevod,
    number_res_perevod,
    number_exp_perevod,
    update_time,
    update_date
)
"""