import time
import random


class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.xp = 0
        self.max_hp = 100
        self.hp = self.max_hp
        self.max_mana = 30
        self.mana = self.max_mana
        self.attack = 10

    def is_alive(self):
        return self.hp > 0

    def gain_xp(self, amount):
        self.xp += amount
        print(f"+{amount} XP")
        self.check_level_up()

    def check_level_up(self):
        needed = self.level * 100
        while self.xp >= needed:
            self.xp -= needed
            self.level += 1
            print(f"\n=== LEVEL UP! Kamu sekarang level {self.level} ===")
            self.level_up_reward()
            needed = self.level * 100

    def level_up_reward(self):
        print("Pilih bonus level up:")
        print("1) Tambah maksimal darah (+30 HP)")
        print("2) Tambah maksimal mana (+15 Mana)")
        print("3) Tambah Attack (+4 Attack)")
        choice = input("Pilihan (1-3): ")
        if choice == '1':
            self.max_hp += 30
            self.hp = self.max_hp
            print("Darah maksimal bertambah! HP disembuhkan penuh.")
        elif choice == '2':
            self.max_mana += 15
            self.mana = self.max_mana
            print("Mana maksimal bertambah! Mana diisi penuh.")
        else:
            self.attack += 4
            print("Attackmu meningkat.")


class Enemy:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def is_alive(self):
        return self.hp > 0


def slow(text, delay=0.02):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()


def combat(player, enemy, xp_reward=50):
    print(f"\n⚔️  Bertarung melawan {enemy.name}! ⚔️")
    while player.is_alive() and enemy.is_alive():
        print(f"\n{player.name}: ❤️ {player.hp}/{player.max_hp}  🔮 {player.mana}/{player.max_mana}  ⭐ Lv{player.level}")
        print(f"{enemy.name}: ❤️ {enemy.hp}")
        print("1) ⚒️ Serang biasa")
        print("2) 🔥 Serangan sihir (Fireball, -10 Mana)")
        print("3) 🏃 Coba kabur")
        cmd = input("Pilihanmu: ")
        if cmd == '1':
            dmg = player.attack + random.randint(-2, 3)
            enemy.hp -= max(1, dmg)
            print(f"Kamu menyerang dan memberi {max(1,dmg)} damage.")
        elif cmd == '2' and player.mana >= 10:
            player.mana -= 10
            dmg = player.attack * 2 + random.randint(0, 5)
            enemy.hp -= dmg
            print(f"🔥 Fireball! Memberi {dmg} damage.")
        elif cmd == '3':
            if random.random() < 0.5:
                print("Berhasil kabur! Kamu melarikan diri ke tempat aman.")
                return False
            else:
                print("Gagal kabur! Musuh masih di belakangmu.")
        else:
            print("Pilihan tidak valid atau mana tidak cukup.")

        if enemy.is_alive():
            edmg = enemy.attack + random.randint(-2, 2)
            player.hp -= max(1, edmg)
            print(f"{enemy.name} menyerang dan memberi {max(1,edmg)} damage.")

    if player.is_alive():
        print(f"🎉 Kamu menang melawan {enemy.name}! 🎉")
        player.gain_xp(xp_reward)
        # Pulihkan sedikit HP/Mana setelah menang
        heal_hp = min(player.max_hp - player.hp, 10)
        heal_m = min(player.max_mana - player.mana, 5)
        player.hp += heal_hp
        player.mana += heal_m
        print(f"Pulih {heal_hp} HP dan {heal_m} Mana.")
        return True
    else:
        print("💀 Kamu tewas... Permainan selesai.")
        return False


def build_story():
    # tiap node: text, list of_choices where each choice is (desc, next_node, action)
    # action is a callable(player) or None
    nodes = {}

    nodes['start'] = {
        'text': "Kau berdiri di depan gerbang megah Istana Aurora. Suara bisik-bisik di angin. 🏰🔍",
        'art': r"""
          .-.                                _
         /   \                              | |
        |     |  _   _  _ __   __ _  _   _  | |__   ___  _ __
        |  |  | | | | || '__| / _` || | | | | '_ \ / _ \| '__|
        |  |  | | |_| || |   | (_| || |_| | | |_) |  __/| |
         \___/   \__,_||_|    \__, | \__,_| |_.__/ \___||_|
                             __/ |
                            |___/  """,
        'choices': [
            ("Masuk diam-diam lewat gerbang samping.", 'hallway', None),
            ("Bicara dengan penjaga; tunjukkan surat tugas.", 'guard', None),
            ("Mengamati taman, mencari petunjuk.", 'garden', None)
        ]
    }

    nodes['hallway'] = {
        'text': "Koridor tua, lampu temaram. Ada jejak darah di lantai. 🕯️🩸",
        'art': r"""
         |||||||||||||||||||||||||
         |  _   _   _   _   _   |
         | |_| |_| |_| |_| |_| |
         |                   o |
         |_____________________|
        """,
        'choices': [
            ("Ikuti jejak darah.", 'library', lambda p: encounter_skeleton(p)),
            ("Periksa lukisan dekat dinding.", 'painting', None),
            ("Kembali ke gerbang.", 'start', None)
        ]
    }

    nodes['guard'] = {
        'text': "Penjaga memandangmu curiga, lalu menunjuk ke aula utama.",
        'choices': [
            ("Masuk ke aula utama.", 'throne', None),
            ("Tanyakan soal korban.", 'interrogate', None),
            ("Cobalah menyuap penjaga.", 'bribe', lambda p: bribe_guard(p))
        ]
    }

    nodes['garden'] = {
        'text': "Taman malam, angin membawa aroma mawar. Seutas kain tersangkut. 🌹🌙",
        'art': r"""
          .-.
         /   \   _.._    _
        |     |.'  _ '. / |\
         \   / | / \ |\  /
          `-'  |_|_|_| \/
        """,
        'choices': [
            ("Ambil kain dan periksa.", 'veil', None),
            ("Ikuti jejak kaki ke selatan.", 'stable', lambda p: encounter_badger(p)),
            ("Kembali ke gerbang.", 'start', None)
        ]
    }

    nodes['library'] = {
        'text': "Perpustakaan sunyi. Buku-buku tentang racun dan warisan keluarga. 📚🕯️",
        'art': r"""
         ______________________
        /_/_/_/_/_/_/_/_/_/_/_/|
        |  _   _   _   _   _  ||
        | |_| |_| |_| |_| |_| ||
        |  _   _   _   _   _  ||
        | |_| |_| |_| |_| |_| ||
        |_____________________||
        """,
        'choices': [
            ("Cari buku catatan korban.", 'clue', None),
            ("Tiba-tiba ada bayangan — musuh!", 'combat1', lambda p: encounter_guard(p)),
            ("Keluar dan lanjutkan penyelidikan.", 'hallway', None)
        ]
    }

    nodes['painting'] = {
        'text': "Di balik lukisan ada pintu kecil yang menuju ruang servis.",
        'choices': [
            ("Masuk ke ruang servis.", 'servant', None),
            ("Tutup lagi dan lanjutkan.", 'hallway', None),
            ("Periksa lukisan lebih teliti.", 'secret', None)
        ]
    }

    nodes['throne'] = {
        'text': "Aula utama. Tumpukan bunga dan kursi kosong di singgasana. 👑🌸",
        'art': r"""
         _.-^^---....,,--
     _--                  --_
    <                        >)
    |                         |
     \._                   _./
        ```--. . , ; .--''
              | |   |
           .-=||  | |=-.
           `-=#$%&%$#=-'
              | ;  :|
     _____.,-#%&$@%#&#~,._____
        """,
        'choices': [
            ("Periksa singgasana.", 'throne_clue', None),
            ("Tanya pelayan di sudut.", 'servant', None),
            ("Tunggu dan amati.", 'ambush', lambda p: encounter_assassin(p))
        ]
    }

    nodes['interrogate'] = {
        'text': "Penjaga bercerita tentang malam yang gelap; samar-samar menyebut nama 'Adelina'.",
        'choices': [
            ("Catat nama itu dan lanjutkan.", 'start', None),
            ("Tanya lebih detail.", 'detailedup', None),
            ("Abaikan dan masuk.", 'throne', None)
        ]
    }

    nodes['bribe'] = {
        'text': "Penjaga menerima sedikit koin dan menutup mata — kau diberi akses lebih.",
        'choices': [
            ("Masuk ke area dalam.", 'innercourt', None),
            ("Mencari informasi dari penjaga.", 'guardinfo', None),
            ("Kembali.", 'start', None)
        ]
    }

    nodes['veil'] = {
        'text': "Kain itu berlambang istana; ada noda darah samar.",
        'choices': [
            ("Bawa ke penjaga.", 'guard', None),
            ("Simpan sebagai bukti.", 'start', None),
            ("Lanjutkan ke taman.", 'garden', None)
        ]
    }

    nodes['stable'] = {
        'text': "Kandang kuda, ada kuda yang gelisah dan bekas darah.",
        'choices': [
            ("Periksa kuda.", 'horse', None),
            ("Tanya tukang kuda.", 'groom', None),
            ("Kembali ke taman.", 'garden', None)
        ]
    }

    nodes['combat1'] = {
        'text': "Pertarungan singkat selesai.",
        'choices': [
            ("Lanjutkan ke perpustakaan.", 'library', None),
            ("Istirahat sejenak.", 'start', None),
            ("Periksa musuh yang tumbang.", 'loot', None)
        ]
    }

    nodes['servant'] = {
        'text': "Pelayan mengingat seseorang yang sering lewat ke ruang rahasia.",
        'choices': [
            ("Tanyakan nama.", 'nameclue', None),
            ("Ikuti arah yang diberikan.", 'secretroom', None),
            ("Kembali ke aula.", 'throne', None)
        ]
    }

    nodes['secretroom'] = {
        'text': "Ruang kecil penuh dokumen. Ada bukti dan surat ancaman.",
        'choices': [
            ("Baca surat ancaman.", 'finalclue', None),
            ("Ambil bukti.", 'end_solve', lambda p: p.gain_xp(150)),
            ("Keluar tanpa mengganggu.", 'servant', None)
        ]
    }

    nodes['end_solve'] = {
        'text': "Dengan bukti di tangan, kau mengungkap pelaku — misteri terpecahkan!",
        'choices': [
            ("Tamat — rayakan kemenangan.", 'the_end', None),
            ("Simpan bukti dan tinggalkan istana.", 'the_end', None),
            ("Periksa ulang bukti.", 'secretroom', None)
        ]
    }

    nodes['the_end'] = {
        'text': "Kisah berakhir. Kau dipuji sebagai detektif istana.",
        'choices': [
            ("Main lagi.", 'start', None),
            ("Keluar.", None, None),
            ("Cek status.", None, None)
        ]
    }

    # Tambahan node pendukung
    nodes['clue'] = {
        'text': "Dalam catatan: ada lalu lintas gelap antara kamar sang bangsawan dan taman.",
        'choices': [
            ("Catat dan kembali ke perpustakaan.", 'library', None),
            ("Bawa bukti ke penjaga.", 'guard', None),
            ("Telusuri nama yang tercatat.", 'nameclue', None)
        ]
    }

    nodes['secret'] = {
        'text': "Ada kode kecil terukir; tampaknya mengarah ke ruang bawah tanah.",
        'choices': [
            ("Catat kode dan kembali.", 'painting', None),
            ("Ikuti jejak ke ruang rahasia.", 'secretroom', None),
            ("Tutup pintu dan pergi.", 'hallway', None)
        ]
    }

    nodes['throne_clue'] = {
        'text': "Di bawah bantal singgasana ada surat sobek yang menyebutkan pertemuan di malam hari.",
        'choices': [
            ("Ambil surat.", 'throne', None),
            ("Tanyakan pada pelayan.", 'servant', None),
            ("Simpan sebagai bukti.", 'start', None)
        ]
    }

    nodes['ambush'] = {
        'text': "Saat menunggu, seseorang melompat—kamu diserang! ⚔️",
        'choices': [
            ("Lawan!", 'throne', lambda p: encounter_assassin(p)),
            ("Lari ke luar.", 'start', None),
            ("Bersembunyi.", 'throne', None)
        ]
    }

    nodes['nameclue'] = {
        'text': "Nama yang disebut pelayan: 'Adelina'. Sebuah petunjuk kuat. 📝",
        'choices': [
            ("Catat nama.", 'start', None),
            ("Cari siapa Adelina.", 'secretroom', None),
            ("Tanya lagi.", 'servant', None)
        ]
    }

    nodes['finalclue'] = {
        'text': "Surat ancaman menyebut 'warisan' dan 'pesta topeng' — petunjuk menuju tersangka.",
        'choices': [
            ("Bawa bukti ke pengadilan.", 'end_solve', None),
            ("Simpan dan selidiki lebih jauh.", 'secretroom', None),
            ("Kembali.", 'servant', None)
        ]
    }

    nodes['horse'] = {
        'text': "Kuda terluka—ada bekas darah yang cocok dengan kain yang ditemukan.",
        'choices': [
            ("Bawa kuda ke tukang.", 'groom', None),
            ("Periksa lagi kuda.", 'stable', None),
            ("Kembali ke taman.", 'garden', None)
        ]
    }

    nodes['groom'] = {
        'text': "Tukang kuda curiga melihat seseorang meninggalkan kuda tercepat pada malam itu.",
        'choices': [
            ("Tanyakan siapa.", 'nameclue', None),
            ("Terima jawaban.", 'garden', None),
            ("Kembali.", 'start', None)
        ]
    }

    nodes['loot'] = {
        'text': "Dari musuh yang tumbang kamu menemukan kunci kecil dan beberapa koin. 💰",
        'choices': [
            ("Ambil kunci.", 'library', None),
            ("Periksa koin.", 'library', None),
            ("Kembali.", 'start', None)
        ]
    }

    nodes['innercourt'] = {
        'text': "Area dalam istana; akses terbatas. Ada pelayan yang gugup.",
        'choices': [
            ("Tanya pelayan.", 'servant', None),
            ("Intip ke jendela.", 'throne', None),
            ("Kembali.", 'start', None)
        ]
    }

    nodes['guardinfo'] = {
        'text': "Penjaga membisik: 'Ada pesta topeng minggu lalu, banyak tamu misterius.'",
        'choices': [
            ("Catat info.", 'start', None),
            ("Tanya lebih lanjut.", 'interrogate', None),
            ("Kembali.", 'start', None)
        ]
    }

    return nodes


def encounter_skeleton(player):
    enemy = Enemy('Penjaga Bayangan', 40, 8)
    return combat(player, enemy, xp_reward=60)


def encounter_guard(player):
    enemy = Enemy('Penjaga Istana', 50, 9)
    return combat(player, enemy, xp_reward=70)


def encounter_badger(player):
    enemy = Enemy('Binatang Liar', 30, 6)
    return combat(player, enemy, xp_reward=40)


def encounter_assassin(player):
    enemy = Enemy('Assassin Misterius', 65, 12)
    return combat(player, enemy, xp_reward=120)


def bribe_guard(player):
    print("Kau memberikan beberapa koin. Penjaga terlihat lega dan membiarkanmu lewat.")
    player.gain_xp(20)


def game_loop(player, nodes):
    current = 'start'
    visited = set()
    while current:
        node = nodes.get(current)
        if not node:
            break
        print('\n' + '—' * 48)
        # show art if any
        if 'art' in node:
            print(node['art'])
        slow('\n' + node['text'])
        # status
        print(f"\nStatus: ❤️ {player.hp}/{player.max_hp}   🔮 {player.mana}/{player.max_mana}   ⭐ Lv{player.level}   XP {player.xp}")
        choices = node['choices']
        for i, (desc, _, _) in enumerate(choices, start=1):
            print(f"{i}) {desc}")

        sel = input("Pilih jalan (1-3): ")
        if sel not in ['1', '2', '3']:
            print("Masukkan 1, 2, atau 3.")
            continue
        idx = int(sel) - 1
        desc, nxt, action = choices[idx]
        if action:
            ok = action(player)
            # action may return False if player fled; handle gracefully
            if ok is False:
                if not player.is_alive():
                    return
                print("Kamu kembali ke tempat sebelumnya. 🔙")
                time.sleep(0.6)
                continue
        if nxt is None:
            if current == 'the_end' and sel == '2':
                print("Sampai jumpa!")
                return
            if current == 'the_end' and sel == '3':
                print(f"Status: Level {player.level}, HP {player.hp}/{player.max_hp}, Mana {player.mana}/{player.max_mana}, XP {player.xp}")
                continue
            # fallback
            return
        current = nxt


def game_utama():
    print("--- MYSTERY ADVENTURE: ISTANA AURORA ---")
    nama = input("Masukkan namamu, petualang: ")
    player = Player(nama)
    slow(f"Selamat datang, {player.name}. Kamu adalah petualang yang ditugaskan ke Istana Aurora.")
    slow("Tugas utamamu: selesaikan misteri pembunuhan yang mengguncang istana.")
    slow("Kamu memiliki darah (HP), mana untuk sihir, dan kemampuan menyerang. Kalahkan musuh, kumpulkan bukti, dan naik level.")
    nodes = build_story()
    game_loop(player, nodes)


if __name__ == "__main__":
    game_utama()