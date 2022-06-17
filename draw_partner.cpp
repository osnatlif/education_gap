#include "draw_partner.h"
#include "data.h"
#include "global_params.h"
#include "random_values.h"
#include "math.h"
#include "assert.h"

draw_partner_result_t draw_partner(int t, int draw_f_or_b , int age, int in_school_at_t_minus_1, int IND_S, int sex)
{
    draw_partner_result_t result;
    result.CHOOSE_PARTNER=0;
    result.PARTNER_N=0;
    result.ability_p=0;
    result.PS=0;
    result.P_HSD=0;
    result.P_HSG=0;
    result.P_SC=0;
    result.P_CG=0;
    result.P_PC=0;
    result.year_of_school_p=0;
    result.PK=0;
    result.prev_state_p=0;
    result.capacity_p = 0;
    result.PARTNER_P=0;
    result.P_GOOD=0;
    result.P_FAIR=0;
    result.P_POOR=0;
    result.P_HEALTH=GOOD;
    result.Q_UTILITY_PERMANENT=0;
    ////////////////////////////
    // prob of meeting a husband
    ////////////////////////////
    if (sex == 1)   // choose husband
    {
        float match_educ_prob[4][4];
        for (auto i = 0; i < 4; ++i)
        {
            for (auto j = 0; j < 4; ++j)
            {
                match_educ_prob[i][j] = 0.0;
            }
        }

        match_educ_prob[1][1] = exp(omega4_w)/(1.0+exp(omega4_w)+exp(omega7_w));                           //probability of meeting cg if cg
        match_educ_prob[1][2] = exp(omega7_w)/(1.0+exp(omega4_w)+exp(omega7_w));                           //probability of meeting sc if cg
        match_educ_prob[1][3] = 1.0/(1.0+exp(omega4_w)+exp(omega7_w));                                       //probability of meeting hs if cg
        match_educ_prob[2][1] = exp(omega4_w+omega5_w)/(1.0+exp(omega4_w+omega5_w)+exp(omega7_w));         //probability of meeting cg if sc
        match_educ_prob[2][2] =          exp(omega7_w)/(1.0+exp(omega4_w+omega5_w)+exp(omega7_w));         //probability of meeting sc if sc
        match_educ_prob[2][3] =                      1.0/(1.0+exp(omega4_w+omega5_w)+exp(omega7_w));         //probability of meeting hs if sc
        match_educ_prob[3][1] = exp(omega4_w+omega6_w)/(1.0+exp(omega4_w+omega6_w)+exp(omega7_w+omega8_w));//probability of meeting cg if hs
        match_educ_prob[3][2] = exp(omega7_w+omega8_w)/(1.0+exp(omega4_w+omega6_w)+exp(omega7_w+omega8_w));//probability of meeting sc if hs
        match_educ_prob[3][3] =                      1.0/(1.0+exp(omega4_w+omega6_w)+exp(omega7_w+omega8_w));//probability of meeting hs if hs
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        // if not married DRAW HUSBAND + HUSBAND CHARACTERISTICS
        // h_draws = rand(DRAW_F,T,5)
        //1 - MEET HUSBAND
        //2 - HUSBAND SCHOOLING+EXP
        //3 - HUSBAND ABILITY
        //4 - HUSBAND CHILDREN
        //5 - HEALTH
        //6 - PARENTS EDUCATION
        //7 - job offer
        //8 - part time/full time
        //9 - prev state husband
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        float temp;
        if (age < 20)
        {
            temp = (exp(omega1))/(1.0+exp(omega1));
        }
        else if (in_school_at_t_minus_1 == 1 && age > 19)
        {
            float temp1 = omega2 + omega9_w*age + omega10_w*age*age;
            temp = (exp(temp1))/(1.0+exp(temp1));
        }
        else
        {
            float temp1 = omega3 + omega9_w*age + omega10_w*age*age;
            temp = (exp(temp1))/(1.0+exp(temp1));
        }

        if (h_draws(draw_f_or_b,t,1) > temp)  // probability of meeting potential partner a function of age and whether completed schoolings
        {
            result.CHOOSE_PARTNER = 0;
            result.PARTNER_N = 0;
        }
        else
        { //   meet potential husband
            result.CHOOSE_PARTNER = 1;
            result.ability_p = normal_arr[(int)h_draws(draw_f_or_b,t,3)]*sigma(2,2); // draw potential partner ability
            // draw husband educ
            float husbans_p[4];
            float WS = IND_S;
            if ((WS > 0) && (WS < 3))
            {
                husbans_p[1]=match_educ_prob[3][1];
                husbans_p[2]=match_educ_prob[3][2];
                husbans_p[3]=match_educ_prob[3][3];
            }
            else if (WS == 3)
            {
                husbans_p[1]=match_educ_prob[2][1];
                husbans_p[2]=match_educ_prob[2][2];
                husbans_p[3]=match_educ_prob[2][3];
            }
            else if ((WS > 3) && (WS < 6))
            {
                husbans_p[1]=match_educ_prob[1][1];
                husbans_p[2]=match_educ_prob[1][2];
                husbans_p[3]=match_educ_prob[1][3];
            }
            else
            {
                assert(0);
            }

            if (h_draws(draw_f_or_b,t,2) < husbans_p[1])//husband schooling HSD
            {
                if (WS > 1)
                {
                    result.PS = 2;
                    result.P_HSG=1;
                    result.year_of_school_p = 12;
                }
                else
                {
                    result.PS = 1;
                    result.P_HSD=1;
                    result.year_of_school_p = 11;
                }
            }
            else if (h_draws(draw_f_or_b,t,2) > husbans_p[1] && h_draws(draw_f_or_b,t,2) < (husbans_p[1] + husbans_p[2]))//husband schooling HSD
            {
                result.PS = 3;
                result.P_SC = 1;
                result.year_of_school_p = 14;
            }
            else if (h_draws(draw_f_or_b,t,2) > (husbans_p[1] + husbans_p[2]))//husband schooling PC
            {
                if (WS < 5)
                {
                    result.PS = 4;
                    result.P_CG = 1;
                    result.year_of_school_p = 15;
                }
                else
                {
                    result.PS = 5;
                    result.P_PC = 1;
                    result.year_of_school_p = 17;
                }
            }
            // choose potential experience for husband
            int pot_exp = age - result.year_of_school_p - 6;
            if (pot_exp < 3)
            {
                result.PK = HK1;    //HK1 = 1;                              //0-2 years of experience

            }
            else if (pot_exp > 2 && pot_exp < 7)
            {
                result.PK = HK2;    //HK2 = 4;	                          //3-5 years of experience
            }
            else if (pot_exp > 6 && pot_exp < 10)
            {
                result.PK = HK3;    //HK3 = 8;	                          //6-10 years of experience
            }
            else if (pot_exp > 9)
            {
                result.PK = HK4;    //HK4 = 12;	                          //11+ years of experience
            }
            else
            {
                assert(0);
            }

            // draw previous state for husband
            if (h_draws(draw_f_or_b,t,9) < husband_prev_emp(t))
            {
                result.prev_state_p = 1;
                result.capacity_p = 1;
            }
            else if (h_draws(draw_f_or_b,t,9) >= husband_prev_emp(t))
            {
                result.prev_state_p = 0;
            }
            else
            {
                assert(0);
            }

            // draw potential partner children
            result.PARTNER_N = 0;
            if (h_draws(draw_f_or_b,t,4) < husband_prev_kids(t,1))
            {
                result.PARTNER_N = 0;
            }
            else if (h_draws(draw_f_or_b,t,4) > husband_prev_kids(t,1))
            {
                result.PARTNER_N = 1;
            }
            else
            {
                assert(0);
            }

            if (h_draws(draw_f_or_b,t,6) < p_education)
            {
                result.PARTNER_P = 1;   // husband's parents have collage education
            }
            else
            {
                result.PARTNER_P = 0; //husband's parents have only high school education
            }
            // draw husband or potential husband health
            result.P_GOOD = 0;
            result.P_FAIR = 0;
            result.P_POOR = 0;
            if (h_draws(draw_f_or_b,t,5) < health_h(t,2))
            {
                result.P_HEALTH = GOOD;
                result.P_GOOD = 1;
            }
            else if (h_draws(draw_f_or_b,t,5) > health_h(t,2) && h_draws(draw_f_or_b,t,5) < health_h(t,3))
            {
                result.P_HEALTH = FAIR;
                result.P_FAIR = 1;
            }
            else if (h_draws(draw_f_or_b,t,5) > health_h(t,3) && h_draws(draw_f_or_b,t,5) < health_h(t,4))
            {
                result.P_HEALTH = POOR;
                result.P_POOR = 1;
            }
            else
            {
                assert(0);
            }
        }  // close if got an offer - at this stage if CHOOSE_PARTNER=1 we already draw all marriage characteristics - M vector at paper
        ////////////////////////////////////////////////////////////////////////////////////////////////////////
        //    prob of meeting a wife
        ////////////////////////////////////////////////////////////////////////////////////////////////////////
    }
    else
    {
        // choose wife
        float match_educ_prob[4][4];
        for (auto i = 0; i < 4; ++i)
        {
            for (auto j = 0; j < 4; ++j)
            {
                match_educ_prob[i][j] = 0.0;
            }
        }

        match_educ_prob[1][1] = exp(omega4_h)/(1.0+exp(omega4_h)+exp(omega7_h));
        match_educ_prob[1][2] = exp(omega7_h)/(1.0+exp(omega4_h)+exp(omega7_h));
        match_educ_prob[1][3] = 1.0/(1.0+exp(omega4_h)+exp(omega7_h));
        match_educ_prob[2][1] = exp(omega4_h+omega5_h)/(1.0+exp(omega4_h+omega5_h)+exp(omega7_h));
        match_educ_prob[2][2] =          exp(omega7_h)/(1.0+exp(omega4_h+omega5_h)+exp(omega7_h));
        match_educ_prob[2][3] =                      1.0/(1.0+exp(omega4_h+omega5_h)+exp(omega7_h));
        match_educ_prob[3][1] = exp(omega4_h+omega6_h)/(1.0+exp(omega4_h+omega6_h)+exp(omega7_h+omega8_h));
        match_educ_prob[3][2] = exp(omega7_h+omega8_h)/(1.0+exp(omega4_h+omega6_h)+exp(omega7_h+omega8_h));
        match_educ_prob[3][3] =                      1.0/(1.0+exp(omega4_h+omega6_h)+exp(omega7_h+omega8_h));
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        // if not married DRAW HUSBAND + HUSBAND CHARACTERISTICS
        // h_draws = rand(DRAW_F,T,5);
        //1 - MEET HUSBAND;
        //2 - HUSBAND SCHOOLING+EXP;
        //3 - HUSBAND ABILITY;
        //4 - HUSBAND CHILDREN;
        //5 - HEALTH ;
        //6 - PARENTS EDUCATION;
        //7 - job offer;
        //8 - part time/full time;
        //9 - prev state husband
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        float temp;
        if (age < 20)
        {
            temp = (exp(omega1))/(1.0+exp(omega1));
        }
        else if (in_school_at_t_minus_1 == 1 && age > 19)
        {
            float temp1 = omega2 + omega9_h*age + omega10_h*age*age;
            temp = (exp(temp1))/(1.0+exp(temp1));
        }
        else
        {
            float temp1 = omega3 + omega9_h*age + omega10_h*age*age;
            temp = (exp(temp1))/(1.0+exp(temp1));
        }

        if (w_draws(draw_f_or_b,t,4+1) > temp)  // probability of meeting potential partner a function of age and whether completed schoolings
        {
            result.CHOOSE_PARTNER = 0;
            result.Q_UTILITY_PERMANENT = 0;
            result.PARTNER_N = 0;
        }
        else
        { //   meet potential husband
            result.CHOOSE_PARTNER = 1;
            result.Q_UTILITY_PERMANENT =  w_draws(draw_f_or_b,t,4);//  permanent component that is a part of the marriage offer
            result.ability_p = normal_arr[(int)w_draws(draw_f_or_b,t,4+3)]*sigma(2,2); // draw potential partner ability
            // draw husband educ
            float wife_p[4];
            float WS = IND_S;
            if ((WS > 0) && (WS < 3))
            {
                wife_p[1] = match_educ_prob[3][1];
                wife_p[2] = match_educ_prob[3][2];
                wife_p[3] = match_educ_prob[3][3];
            }
            else if (WS == 3)
            {
                wife_p[1] = match_educ_prob[2][1];
                wife_p[2] = match_educ_prob[2][2];
                wife_p[3] = match_educ_prob[2][3];
            }
            else if ((WS > 3) && (WS < 6))
            {
                wife_p[1] = match_educ_prob[1][1];
                wife_p[2] = match_educ_prob[1][2];
                wife_p[3] = match_educ_prob[1][3];
            }
            else
            {
                assert(0);
            }

            if (w_draws(draw_f_or_b,t,4+2) < wife_p[1])//husband schooling HSD
            {
                if (WS > 1)
                {
                    result.PS = 2;
                    result.P_HSG = 1;
                    result.year_of_school_p = 12;
                }
                else
                {
                    result.PS = 1;
                    result.P_HSD = 1;
                    result.year_of_school_p = 11;
                }
            }
            else if (w_draws(draw_f_or_b,t,4+2) > wife_p[1] && w_draws(draw_f_or_b,t,4+2) < (wife_p[1]+wife_p[2]))//husband schooling HSD
            {
                result.PS = 3;
                result.P_SC = 1;
                result.year_of_school_p = 14;
            }
            else if (w_draws(draw_f_or_b,t,4+2) > (wife_p[1]+wife_p[2]))//husband schooling PC
            {
                if (WS < 5)
                {
                    result.PS = 4;
                    result.P_CG = 1;
                    result.year_of_school_p = 15;
                }
                else
                {
                    result.PS = 5;
                    result.P_PC = 1;
                    result.year_of_school_p = 17;
                }
            }

            //  choose potential experience for husband
            int pot_exp = age - result.year_of_school_p - 6;
            if (pot_exp < 3)
            {
                result.PK = HK1;    //HK1 = 1;                              //0-2 years of experience
            }
            else if (pot_exp > 2 && pot_exp < 7)
            {
                result.PK = HK2;    //HK2 = 4;	                          //3-5 years of experience
            }
            else if (pot_exp > 6 && pot_exp < 10)
            {
                result.PK = HK3;    //HK3 = 8;	                          //6-10 years of experience
            }
            else if (pot_exp  > 9   )
            {
                result.PK = HK4;    //HK4 = 12;	                          //11+ years of experience
            }
            else
            {
                assert(0);
            }

            // draw previous state for husband
            if (w_draws(draw_f_or_b,t,4+7)<wife_prev_emp(t))
            {
                result.prev_state_p = 1;
            }
            else if (w_draws(draw_f_or_b,t,4+7)>= wife_prev_emp(t))
            {
                result.prev_state_p = 0;
            }
            else
            {
                assert(0);
            }

            // draw potential partner children
            result.PARTNER_N = 0;
            if (w_draws(draw_f_or_b,t,4+4) < wife_prev_kids(t,1))
            {
                result.PARTNER_N = 0;
            }
            else if (w_draws(draw_f_or_b,t,4+4) > wife_prev_kids(t,1))
            {
                result.PARTNER_N = 1;
            }
            else
            {
                assert(0);
            }

            if (w_draws(draw_f_or_b,t,4+6)<p_education)
            {
                result.PARTNER_P = 1;   // husband's parents have collage education
            }
            else
            {
                result.PARTNER_P = 0; //husband's parents have only high school education
            }

            // draw husband or potential husband health
            result.P_GOOD = 0; result.P_FAIR = 0; result.P_POOR = 0;
            if (w_draws(draw_f_or_b,t,4+5)<health_w(t,2))
            {
                result.P_HEALTH = GOOD;
                result.P_GOOD = 1;
            }
            else if (w_draws(draw_f_or_b,t,4+5)>health_w(t,2) && w_draws(draw_f_or_b,t,4+5)<health_w(t,3))
            {
                result.P_HEALTH = FAIR;
                result.P_FAIR = 1;
            }
            else if (w_draws(draw_f_or_b,t,4+5)>health_w(t,3) && w_draws(draw_f_or_b,t,4+5)<health_w(t,4))
            {
                result.P_HEALTH = POOR;
                result.P_POOR = 1;
            }
            else
            {
                assert(0);
            }
        }  // close if got an offer - at this stage if CHOOSE_PARTNER=1 we already draw all marriage characteristics - M vector at paper
    }

    return result;
}

