import random

class pa_simulator:

#    def __init__(self, pitch, swing, pitcher, batter, brc, result):
    def __init__(self, brc, result):
#        self.pitch = int(pitch)
#        self.swing = int(swing)
#        self.pitcher = pitcher.split('|')
#        self.batter = batter.split('|')
        self.brc = int(brc)
        self.result = result
        self.pitch_rand = ['ball'] * 363 + ['looking'] * 168 + ['swung'] * 117 + ['foul'] * 177 + ['inplay'] * 175

    def sim_inplay(self):
        

    def sim_count(self):
        count_history = []
        balls = 0
        strikes = 0
        done = 'no'
        if self.result == 'k':
            while done == 'no':
                pitch = self.sim_pitch(balls,strikes)
                if pitch == 'ball' and balls < 3:
                    balls += 1
                    count_history.append(pitch)
                elif (pitch == 'looking' or pitch == 'swung'):
                    strikes += 1
                    count_history.append(pitch)
                elif pitch == 'foul':
                    if strikes < 2:
                        strikes += 1
                    count_history.append(pitch)
                if strikes == 3:
                    done = 'yes'
        elif self.result == 'bb':
            while done == 'no':
                pitch = self.sim_pitch(balls,strikes)
                if pitch == 'ball':
                    balls += 1
                    count_history.append(pitch)
                elif (pitch == 'looking' or pitch == 'swung') and strikes < 2:
                    strikes += 1
                    count_history.append(pitch)
                elif pitch == 'foul':
                    if strikes < 2:
                        strikes += 1
                    count_history.append(pitch)
                if balls == 4:
                    done = 'yes'
        else:
            while done == 'no':
                pitch = self.sim_pitch(balls,strikes)
                if pitch == 'ball' and balls < 3:
                    balls += 1
                    count_history.append(pitch)
                elif (pitch == 'looking' or pitch == 'swung') and strikes < 2:
                    strikes += 1
                    count_history.append(pitch)
                elif pitch == 'foul':
                    if strikes < 2:
                        strikes += 1
                    count_history.append(pitch)
                elif pitch == 'inplay':
                    count_history.append(pitch)
                    done = 'yes'
        return self.result, balls, strikes, count_history

    def sim_pitch(self,balls=0,strikes=0):
        pitch = random.choice(self.pitch_rand)
        return pitch