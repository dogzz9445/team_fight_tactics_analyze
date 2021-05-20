from sqlalchemy import Column, String, Numeric, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

from .base import Base

class Match(Base):
    __tablename__ = 'analyze_set5'

    id = Column(Integer, primary_key=True)
    Set5_Assassin_num_units = Column(TINYINT)
    Set5_Assassin_tier_current = Column(TINYINT)
    Set5_Brawler_num_units = Column(TINYINT)
    Set5_Brawler_tier_current = Column(TINYINT)
    Set5_Caretaker_num_units = Column(TINYINT)
    Set5_Caretaker_tier_current = Column(TINYINT)
    Set5_Coven_num_units = Column(TINYINT)
    Set5_Coven_tier_current = Column(TINYINT)
    Set5_Dawnbringer_num_units = Column(TINYINT)
    Set5_Dawnbringer_tier_current = Column(TINYINT)
    Set5_Draconic_num_units = Column(TINYINT)
    Set5_Draconic_tier_current = Column(TINYINT)
    Set5_Eternal_num_units = Column(TINYINT)
    Set5_Eternal_tier_current = Column(TINYINT)
    Set5_Invoker_num_units = Column(TINYINT)
    Set5_Invoker_tier_current = Column(TINYINT)
    Set5_Mystic_num_units = Column(TINYINT)
    Set5_Mystic_tier_current = Column(TINYINT)
    Set5_Nightbringer_num_units = Column(TINYINT)
    Set5_Nightbringer_tier_current = Column(TINYINT)
    Set5_Renewer_num_units = Column(TINYINT)
    Set5_Renewer_tier_current = Column(TINYINT)
    Set5_Revenant_num_units = Column(TINYINT)
    Set5_Revenant_tier_current = Column(TINYINT)
    TFT5_Vladimir_tier = Column(TINYINT)
    TFT5_Vladimir_exits = Column(TINYINT)
    TFT5_Lissandra_tier = Column(TINYINT)
    TFT5_Lissandra_exits = Column(TINYINT)
    TFT5_Soraka_tier = Column(TINYINT)
    TFT5_Soraka_exits = Column(TINYINT)
    TFT5_LeBlanc_tier = Column(TINYINT)
    TFT5_LeBlanc_exits = Column(TINYINT)
    TFT5_Nocturne_tier = Column(TINYINT)
    TFT5_Nocturne_exits = Column(TINYINT)
    TFT5_Morgana_tier = Column(TINYINT)
    TFT5_Morgana_exits = Column(TINYINT)
    TFT5_Ivern_tier = Column(TINYINT)
    TFT5_Ivern_exits = Column(TINYINT)
    TFT5_Volibear_tier = Column(TINYINT)
    TFT5_Volibear_exits = Column(TINYINT)
    TFT5_Heimerdinger_tier = Column(TINYINT)
    TFT5_Heimerdinger_exits = Column(TINYINT)
    Set5_Cavalier_num_units = Column(TINYINT)
    Set5_Cavalier_tier_current = Column(TINYINT)
    Set5_Cruel_num_units = Column(TINYINT)
    Set5_Cruel_tier_current = Column(TINYINT)
    Set5_Hellion_num_units = Column(TINYINT)
    Set5_Hellion_tier_current = Column(TINYINT)
    Set5_Ironclad_num_units = Column(TINYINT)
    Set5_Ironclad_tier_current = Column(TINYINT)
    Set5_Knight_num_units = Column(TINYINT)
    Set5_Knight_tier_current = Column(TINYINT)
    Set5_Redeemed_num_units = Column(TINYINT)
    Set5_Redeemed_tier_current = Column(TINYINT)
    Set5_Skirmisher_num_units = Column(TINYINT)
    Set5_Skirmisher_tier_current = Column(TINYINT)
    TFT5_Kled_tier = Column(TINYINT)
    TFT5_Kled_exits = Column(TINYINT)
    TFT5_Poppy_tier = Column(TINYINT)
    TFT5_Poppy_exits = Column(TINYINT)
    TFT5_Kennen_tier = Column(TINYINT)
    TFT5_Kennen_exits = Column(TINYINT)
    TFT5_Nautilus_tier = Column(TINYINT)
    TFT5_Nautilus_exits = Column(TINYINT)
    TFT5_Lulu_tier = Column(TINYINT)
    TFT5_Lulu_exits = Column(TINYINT)
    TFT5_Rell_tier = Column(TINYINT)
    TFT5_Rell_exits = Column(TINYINT)
    TFT5_Teemo_tier = Column(TINYINT)
    TFT5_Teemo_exits = Column(TINYINT)
    Set5_Dragonslayer_num_units = Column(TINYINT)
    Set5_Dragonslayer_tier_current = Column(TINYINT)
    TFT5_Trundle_tier = Column(TINYINT)
    TFT5_Trundle_exits = Column(TINYINT)
    TFT5_LeeSin_tier = Column(TINYINT)
    TFT5_LeeSin_exits = Column(TINYINT)
    TFT5_Nidalee_tier = Column(TINYINT)
    TFT5_Nidalee_exits = Column(TINYINT)
    TFT5_Pantheon_tier = Column(TINYINT)
    TFT5_Pantheon_exits = Column(TINYINT)
    TFT5_Jax_tier = Column(TINYINT)
    TFT5_Jax_exits = Column(TINYINT)
    TFT5_Diana_tier = Column(TINYINT)
    TFT5_Diana_exits = Column(TINYINT)
    Set5_Forgotten_num_units = Column(TINYINT)
    Set5_Forgotten_tier_current = Column(TINYINT)
    Set5_GodKing_num_units = Column(TINYINT)
    Set5_GodKing_tier_current = Column(TINYINT)
    Set5_Legionnaire_num_units = Column(TINYINT)
    Set5_Legionnaire_tier_current = Column(TINYINT)
    Set5_Verdant_num_units = Column(TINYINT)
    Set5_Verdant_tier_current = Column(TINYINT)
    TFT5_Warwick_tier = Column(TINYINT)
    TFT5_Warwick_exits = Column(TINYINT)
    TFT5_Taric_tier = Column(TINYINT)
    TFT5_Taric_exits = Column(TINYINT)
    TFT5_Mordekaiser_tier = Column(TINYINT)
    TFT5_Mordekaiser_exits = Column(TINYINT)
    TFT5_Darius_tier = Column(TINYINT)
    TFT5_Darius_exits = Column(TINYINT)
    TFT5_Garen_tier = Column(TINYINT)
    TFT5_Garen_exits = Column(TINYINT)
    TFT5_Kayle_tier = Column(TINYINT)
    TFT5_Kayle_exits = Column(TINYINT)
    TFT5_Udyr_tier = Column(TINYINT)
    TFT5_Udyr_exits = Column(TINYINT)
    TFT5_Viego_tier = Column(TINYINT)
    TFT5_Viego_exits = Column(TINYINT)
    Set5_Abomination_num_units = Column(TINYINT)
    Set5_Abomination_tier_current = Column(TINYINT)
    Set5_Ranger_num_units = Column(TINYINT)
    Set5_Ranger_tier_current = Column(TINYINT)
    TFT5_Thresh_tier = Column(TINYINT)
    TFT5_Thresh_exits = Column(TINYINT)
    TFT5_Hecarim_tier = Column(TINYINT)
    TFT5_Hecarim_exits = Column(TINYINT)
    TFT5_Katarina_tier = Column(TINYINT)
    TFT5_Katarina_exits = Column(TINYINT)
    TFT5_Draven_tier = Column(TINYINT)
    TFT5_Draven_exits = Column(TINYINT)
    TFT5_Ryze_tier = Column(TINYINT)
    TFT5_Ryze_exits = Column(TINYINT)
    TFT5_Kindred_tier = Column(TINYINT)
    TFT5_Kindred_exits = Column(TINYINT)
    TFT5_Lux_tier = Column(TINYINT)
    TFT5_Lux_exits = Column(TINYINT)
    TFT5_Khazix_tier = Column(TINYINT)
    TFT5_Khazix_exits = Column(TINYINT)
    Set5_Spellweaver_num_units = Column(TINYINT)
    Set5_Spellweaver_tier_current = Column(TINYINT)
    TFT5_Ziggs_tier = Column(TINYINT)
    TFT5_Ziggs_exits = Column(TINYINT)
    TFT5_Yasuo_tier = Column(TINYINT)
    TFT5_Yasuo_exits = Column(TINYINT)
    TFT5_Kalista_tier = Column(TINYINT)
    TFT5_Kalista_exits = Column(TINYINT)
    TFT5_Brand_tier = Column(TINYINT)
    TFT5_Brand_exits = Column(TINYINT)
    TFT5_Nunu_tier = Column(TINYINT)
    TFT5_Nunu_exits = Column(TINYINT)
    TFT5_Leona_tier = Column(TINYINT)
    TFT5_Leona_exits = Column(TINYINT)
    TFT5_Aatrox_tier = Column(TINYINT)
    TFT5_Aatrox_exits = Column(TINYINT)
    TFT5_Velkoz_tier = Column(TINYINT)
    TFT5_Velkoz_exits = Column(TINYINT)
    TFT5_Vayne_tier = Column(TINYINT)
    TFT5_Vayne_exits = Column(TINYINT)
    TFT5_Viktor_tier = Column(TINYINT)
    TFT5_Viktor_exits = Column(TINYINT)
    TFT5_Varus_tier = Column(TINYINT)
    TFT5_Varus_exits = Column(TINYINT)
    TFT5_Sejuani_tier = Column(TINYINT)
    TFT5_Sejuani_exits = Column(TINYINT)
    TFT5_Aphelios_tier = Column(TINYINT)
    TFT5_Aphelios_exits = Column(TINYINT)
    TFT5_Ashe_tier = Column(TINYINT)
    TFT5_Ashe_exits = Column(TINYINT)
    TFT5_Zyra_tier = Column(TINYINT)
    TFT5_Zyra_exits = Column(TINYINT)
    TFT5_Syndra_tier = Column(TINYINT)
    TFT5_Syndra_exits = Column(TINYINT)
    TFT5_Karma_tier = Column(TINYINT)
    TFT5_Karma_exits = Column(TINYINT)
    TFT5_Sett_tier = Column(TINYINT)
    TFT5_Sett_exits = Column(TINYINT)
    TFT5_Gragas_tier = Column(TINYINT)
    TFT5_Gragas_exits = Column(TINYINT)
    TFT5_Riven_tier = Column(TINYINT)
    TFT5_Riven_exits = Column(TINYINT)
    participant_id = Column(Integer, ForeignKey('participants.id'))

    def fromDataFrame(self, df):
        self.Set5_Assassin_num_units = df['Set5_Assassin_num_units']
        self.Set5_Assassin_tier_current = df['Set5_Assassin_tier_current']
        self.Set5_Brawler_num_units = df['Set5_Brawler_num_units']
        self.Set5_Brawler_tier_current = df['Set5_Brawler_tier_current']
        self.Set5_Caretaker_num_units = df['Set5_Caretaker_num_units']
        self.Set5_Caretaker_tier_current = df['Set5_Caretaker_tier_current']
        self.Set5_Coven_num_units = df['Set5_Coven_num_units']
        self.Set5_Coven_tier_current = df['Set5_Coven_tier_current']
        self.Set5_Dawnbringer_num_units = df['Set5_Dawnbringer_num_units']
        self.Set5_Dawnbringer_tier_current = df['Set5_Dawnbringer_tier_current']
        self.Set5_Draconic_num_units = df['Set5_Draconic_num_units']
        self.Set5_Draconic_tier_current = df['Set5_Draconic_tier_current']
        self.Set5_Eternal_num_units = df['Set5_Eternal_num_units']
        self.Set5_Eternal_tier_current = df['Set5_Eternal_tier_current']
        self.Set5_Invoker_num_units = df['Set5_Invoker_num_units']
        self.Set5_Invoker_tier_current = df['Set5_Invoker_tier_current']
        self.Set5_Mystic_num_units = df['Set5_Mystic_num_units']
        self.Set5_Mystic_tier_current = df['Set5_Mystic_tier_current']
        self.Set5_Nightbringer_num_units = df['Set5_Nightbringer_num_units']
        self.Set5_Nightbringer_tier_current = df['Set5_Nightbringer_tier_current']
        self.Set5_Renewer_num_units = df['Set5_Renewer_num_units']
        self.Set5_Renewer_tier_current = df['Set5_Renewer_tier_current']
        self.Set5_Revenant_num_units = df['Set5_Revenant_num_units']
        self.Set5_Revenant_tier_current = df['Set5_Revenant_tier_current']
        self.TFT5_Vladimir_tier = df['TFT5_Vladimir_tier']
        self.TFT5_Vladimir_exits = df['TFT5_Vladimir_exits']
        self.TFT5_Lissandra_tier = df['TFT5_Lissandra_tier']
        self.TFT5_Lissandra_exits = df['TFT5_Lissandra_exits']
        self.TFT5_Soraka_tier = df['TFT5_Soraka_tier']
        self.TFT5_Soraka_exits = df['TFT5_Soraka_exits']
        self.TFT5_LeBlanc_tier = df['TFT5_LeBlanc_tier']
        self.TFT5_LeBlanc_exits = df['TFT5_LeBlanc_exits']
        self.TFT5_Nocturne_tier = df['TFT5_Nocturne_tier']
        self.TFT5_Nocturne_exits = df['TFT5_Nocturne_exits']
        self.TFT5_Morgana_tier = df['TFT5_Morgana_tier']
        self.TFT5_Morgana_exits = df['TFT5_Morgana_exits']
        self.TFT5_Ivern_tier = df['TFT5_Ivern_tier']
        self.TFT5_Ivern_exits = df['TFT5_Ivern_exits']
        self.TFT5_Volibear_tier = df['TFT5_Volibear_tier']
        self.TFT5_Volibear_exits = df['TFT5_Volibear_exits']
        self.TFT5_Heimerdinger_tier = df['TFT5_Heimerdinger_tier']
        self.TFT5_Heimerdinger_exits = df['TFT5_Heimerdinger_exits']
        self.Set5_Cavalier_num_units = df['Set5_Cavalier_num_units']
        self.Set5_Cavalier_tier_current = df['Set5_Cavalier_tier_current']
        self.Set5_Cruel_num_units = df['Set5_Cruel_num_units']
        self.Set5_Cruel_tier_current = df['Set5_Cruel_tier_current']
        self.Set5_Hellion_num_units = df['Set5_Hellion_num_units']
        self.Set5_Hellion_tier_current = df['Set5_Hellion_tier_current']
        self.Set5_Ironclad_num_units = df['Set5_Ironclad_num_units']
        self.Set5_Ironclad_tier_current = df['Set5_Ironclad_tier_current']
        self.Set5_Knight_num_units = df['Set5_Knight_num_units']
        self.Set5_Knight_tier_current = df['Set5_Knight_tier_current']
        self.Set5_Redeemed_num_units = df['Set5_Redeemed_num_units']
        self.Set5_Redeemed_tier_current = df['Set5_Redeemed_tier_current']
        self.Set5_Skirmisher_num_units = df['Set5_Skirmisher_num_units']
        self.Set5_Skirmisher_tier_current = df['Set5_Skirmisher_tier_current']
        self.TFT5_Kled_tier = df['TFT5_Kled_tier']
        self.TFT5_Kled_exits = df['TFT5_Kled_exits']
        self.TFT5_Poppy_tier = df['TFT5_Poppy_tier']
        self.TFT5_Poppy_exits = df['TFT5_Poppy_exits']
        self.TFT5_Kennen_tier = df['TFT5_Kennen_tier']
        self.TFT5_Kennen_exits = df['TFT5_Kennen_exits']
        self.TFT5_Nautilus_tier = df['TFT5_Nautilus_tier']
        self.TFT5_Nautilus_exits = df['TFT5_Nautilus_exits']
        self.TFT5_Lulu_tier = df['TFT5_Lulu_tier']
        self.TFT5_Lulu_exits = df['TFT5_Lulu_exits']
        self.TFT5_Rell_tier = df['TFT5_Rell_tier']
        self.TFT5_Rell_exits = df['TFT5_Rell_exits']
        self.TFT5_Teemo_tier = df['TFT5_Teemo_tier']
        self.TFT5_Teemo_exits = df['TFT5_Teemo_exits']
        self.Set5_Dragonslayer_num_units = df['Set5_Dragonslayer_num_units']
        self.Set5_Dragonslayer_tier_current = df['Set5_Dragonslayer_tier_current']
        self.TFT5_Trundle_tier = df['TFT5_Trundle_tier']
        self.TFT5_Trundle_exits = df['TFT5_Trundle_exits']
        self.TFT5_LeeSin_tier = df['TFT5_LeeSin_tier']
        self.TFT5_LeeSin_exits = df['TFT5_LeeSin_exits']
        self.TFT5_Nidalee_tier = df['TFT5_Nidalee_tier']
        self.TFT5_Nidalee_exits = df['TFT5_Nidalee_exits']
        self.TFT5_Pantheon_tier = df['TFT5_Pantheon_tier']
        self.TFT5_Pantheon_exits = df['TFT5_Pantheon_exits']
        self.TFT5_Jax_tier = df['TFT5_Jax_tier']
        self.TFT5_Jax_exits = df['TFT5_Jax_exits']
        self.TFT5_Diana_tier = df['TFT5_Diana_tier']
        self.TFT5_Diana_exits = df['TFT5_Diana_exits']
        self.Set5_Forgotten_num_units = df['Set5_Forgotten_num_units']
        self.Set5_Forgotten_tier_current = df['Set5_Forgotten_tier_current']
        self.Set5_GodKing_num_units = df['Set5_GodKing_num_units']
        self.Set5_GodKing_tier_current = df['Set5_GodKing_tier_current']
        self.Set5_Legionnaire_num_units = df['Set5_Legionnaire_num_units']
        self.Set5_Legionnaire_tier_current = df['Set5_Legionnaire_tier_current']
        self.Set5_Verdant_num_units = df['Set5_Verdant_num_units']
        self.Set5_Verdant_tier_current = df['Set5_Verdant_tier_current']
        self.TFT5_Warwick_tier = df['TFT5_Warwick_tier']
        self.TFT5_Warwick_exits = df['TFT5_Warwick_exits']
        self.TFT5_Taric_tier = df['TFT5_Taric_tier']
        self.TFT5_Taric_exits = df['TFT5_Taric_exits']
        self.TFT5_Mordekaiser_tier = df['TFT5_Mordekaiser_tier']
        self.TFT5_Mordekaiser_exits = df['TFT5_Mordekaiser_exits']
        self.TFT5_Darius_tier = df['TFT5_Darius_tier']
        self.TFT5_Darius_exits = df['TFT5_Darius_exits']
        self.TFT5_Garen_tier = df['TFT5_Garen_tier']
        self.TFT5_Garen_exits = df['TFT5_Garen_exits']
        self.TFT5_Kayle_tier = df['TFT5_Kayle_tier']
        self.TFT5_Kayle_exits = df['TFT5_Kayle_exits']
        self.TFT5_Udyr_tier = df['TFT5_Udyr_tier']
        self.TFT5_Udyr_exits = df['TFT5_Udyr_exits']
        self.TFT5_Viego_tier = df['TFT5_Viego_tier']
        self.TFT5_Viego_exits = df['TFT5_Viego_exits']
        self.Set5_Abomination_num_units = df['Set5_Abomination_num_units']
        self.Set5_Abomination_tier_current = df['Set5_Abomination_tier_current']
        self.Set5_Ranger_num_units = df['Set5_Ranger_num_units']
        self.Set5_Ranger_tier_current = df['Set5_Ranger_tier_current']
        self.TFT5_Thresh_tier = df['TFT5_Thresh_tier']
        self.TFT5_Thresh_exits = df['TFT5_Thresh_exits']
        self.TFT5_Hecarim_tier = df['TFT5_Hecarim_tier']
        self.TFT5_Hecarim_exits = df['TFT5_Hecarim_exits']
        self.TFT5_Katarina_tier = df['TFT5_Katarina_tier']
        self.TFT5_Katarina_exits = df['TFT5_Katarina_exits']
        self.TFT5_Draven_tier = df['TFT5_Draven_tier']
        self.TFT5_Draven_exits = df['TFT5_Draven_exits']
        self.TFT5_Ryze_tier = df['TFT5_Ryze_tier']
        self.TFT5_Ryze_exits = df['TFT5_Ryze_exits']
        self.TFT5_Kindred_tier = df['TFT5_Kindred_tier']
        self.TFT5_Kindred_exits = df['TFT5_Kindred_exits']
        self.TFT5_Lux_tier = df['TFT5_Lux_tier']
        self.TFT5_Lux_exits = df['TFT5_Lux_exits']
        self.TFT5_Khazix_tier = df['TFT5_Khazix_tier']
        self.TFT5_Khazix_exits = df['TFT5_Khazix_exits']
        self.Set5_Spellweaver_num_units = df['Set5_Spellweaver_num_units']
        self.Set5_Spellweaver_tier_current = df['Set5_Spellweaver_tier_current']
        self.TFT5_Ziggs_tier = df['TFT5_Ziggs_tier']
        self.TFT5_Ziggs_exits = df['TFT5_Ziggs_exits']
        self.TFT5_Yasuo_tier = df['TFT5_Yasuo_tier']
        self.TFT5_Yasuo_exits = df['TFT5_Yasuo_exits']
        self.TFT5_Kalista_tier = df['TFT5_Kalista_tier']
        self.TFT5_Kalista_exits = df['TFT5_Kalista_exits']
        self.TFT5_Brand_tier = df['TFT5_Brand_tier']
        self.TFT5_Brand_exits = df['TFT5_Brand_exits']
        self.TFT5_Nunu_tier = df['TFT5_Nunu_tier']
        self.TFT5_Nunu_exits = df['TFT5_Nunu_exits']
        self.TFT5_Leona_tier = df['TFT5_Leona_tier']
        self.TFT5_Leona_exits = df['TFT5_Leona_exits']
        self.TFT5_Aatrox_tier = df['TFT5_Aatrox_tier']
        self.TFT5_Aatrox_exits = df['TFT5_Aatrox_exits']
        self.TFT5_Velkoz_tier = df['TFT5_Velkoz_tier']
        self.TFT5_Velkoz_exits = df['TFT5_Velkoz_exits']
        self.TFT5_Vayne_tier = df['TFT5_Vayne_tier']
        self.TFT5_Vayne_exits = df['TFT5_Vayne_exits']
        self.TFT5_Viktor_tier = df['TFT5_Viktor_tier']
        self.TFT5_Viktor_exits = df['TFT5_Viktor_exits']
        self.TFT5_Varus_tier = df['TFT5_Varus_tier']
        self.TFT5_Varus_exits = df['TFT5_Varus_exits']
        self.TFT5_Sejuani_tier = df['TFT5_Sejuani_tier']
        self.TFT5_Sejuani_exits = df['TFT5_Sejuani_exits']
        self.TFT5_Aphelios_tier = df['TFT5_Aphelios_tier']
        self.TFT5_Aphelios_exits = df['TFT5_Aphelios_exits']
        self.TFT5_Ashe_tier = df['TFT5_Ashe_tier']
        self.TFT5_Ashe_exits = df['TFT5_Ashe_exits']
        self.TFT5_Zyra_tier = df['TFT5_Zyra_tier']
        self.TFT5_Zyra_exits = df['TFT5_Zyra_exits']
        self.TFT5_Syndra_tier = df['TFT5_Syndra_tier']
        self.TFT5_Syndra_exits = df['TFT5_Syndra_exits']
        self.TFT5_Karma_tier = df['TFT5_Karma_tier']
        self.TFT5_Karma_exits = df['TFT5_Karma_exits']
        self.TFT5_Sett_tier = df['TFT5_Sett_tier']
        self.TFT5_Sett_exits = df['TFT5_Sett_exits']
        self.TFT5_Gragas_tier = df['TFT5_Gragas_tier']
        self.TFT5_Gragas_exits = df['TFT5_Gragas_exits']
        self.TFT5_Riven_tier = df['TFT5_Riven_tier']
        self.TFT5_Riven_exits = df['TFT5_Riven_exits']
        self.participant_id = df['id']
        return self
