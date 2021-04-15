#!/usr/bin/env python 
from acme_collectors.utils.tone_classifiers import classify_tones 
from unittest import TestCase  
from typing import Dict, List 

article: str = """
The bombing of two schools and five hospitals in Syria allegedly by Russian warplanes has been slammed as a “war crime,” as the ongoing bloodshed diminished hopes for a cease-fire in the conflict.
Up to 50 civilians, including children, died when missiles hit at least five medical buildings and two schools in the Aleppo and Idlib provinces on Monday.
U.N. Secretary General Ban Ki-moon said the raids violated international law and “cast a shadow” over efforts to end Syria's five-year civil war. He did not say who was responsible for the attacks but groups monitoring the conflict suspected the strikes were carried out by Russia, an ally of the Syrian regime.
Russia’s Health Minister Veronika Skvortsova denied Moscow was responsible, saying its military had targeted Islamic State of Iraq and the Levant (ISIL) infrastructure and that she had no reason to believe it had bombed civilians.
“We are confident that [there is] no way it could be done by our defense forces. This contradicts our ideology,” she said.
French Foreign Minister Jean-Marc Ayrault said attacks on health facilities in Syria by the regime or its supporters were “unacceptable and must stop immediately.”
Turkey on Monday separately accused Russia of “an obvious war crime” and warned that there would be consequences if Russia did not immediately end such attacks.
Syria's ambassador to Moscow, Riad Haddad, said the hospital was targeted by a U.S. raid. “American warplanes destroyed it. Russian warplanes had nothing to do with any of it. The information that has been gathered will completely back that up,” he told Russian state television channel Rossiya 24.
The U.S., which, like the U.N., did not specify who carried out the strikes, said two civilian hospitals were hit in northern Syria: one run by medical charity Doctors Without Borders and another in rebel-held Azaz.
“That the Assad regime and its supporters would continue these attacks … casts doubt on Russia's willingness and/or ability to help bring to a stop the continued brutality of the Assad regime against its own people,” the U.S. State Department said.
Syrian President Bashar Assad warned Turkey and Saudi Arabia that any ground invasion of Syria would have “global repercussions” and said sending in troops would not be a “picnic.”
Commenting on an agreement brokered last week by the U.S., Russia and other world powers for a temporary cessation of hostilities, he said, “Cease-fires occur between armies and states but never between a state and terrorists.”
“They say that they want a cease-fire within a week. All right, who will talk to a terrorist organization if it refuses to cease-fire? Who will punish it?”
Assad's comments were his first since the agreement on Friday to bring about a pause in fighting within a week.
Earlier this month, Saudi Arabia and the UAE said they were prepared to send ground troops to Syria to fight ISIL if a U.S.-led coalition targeting the group with airstrikes agreed to the offer.
Russia warned that if foreign troops entered the country, it could lead to a world war.
"""
class TestClassifier(TestCase):

    def test_classify_tone(self):

        response: Dict = list(map(lambda tone: (tone.get('tone'), tone.get('score')) , classify_tones(text=article))) 
        result: List[float] =  [('Fear', 0.36),
                                ('Sadness', 0.96),
                                ('Confident', 0.43),
                                ('Analytical', 0.4493590748290803),
                                ('Tentative', 0.31),
                                ('Analytical', 0.63610357941074),
                                ('Analytical', 0.5353191489361702),
                                ('Analytical', 0.55475),
                                ('Sadness', 0.58),
                                ('Analytical', 0.6341059406498993),
                                ('Fear', 0.43),
                                ('Fear', 0.37),
                                ('Analytical', 0.71475),
                                ('Analytical', 0.6191721158958001),
                                ('Analytical', 0.33475),
                                ('Analytical', 0.6909432550238382),
                                ('Joy', 0.5407001192885269),
                                ('Analytical', 0.344594250053339),
                                ('Joy', 0.6555713378889204)
                               ]
        return self.assertListEqual(result, response) 