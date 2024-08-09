import sympy as sp
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='puzzle')

@app.route('/')
def index():
    return render_template('puzzle.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # テキストボックスから値を取得
        number = str(request.form['number'])

        # 小数点以下の桁数を指定して円周率を取得
        pi_str = str(sp.N(sp.pi, 10002))

        # 小数点以下の部分のみを取得
        pi_decimal = pi_str.split('.')[1]

        # 任意の数列が出現する位置を検索
        def find_sequence(sequence, pi_decimal):
            positions = []
            seq_len = len(sequence)
            for i in range(len(pi_decimal) - seq_len + 1):
                if pi_decimal[i:i+seq_len] == sequence:
                    row = i // 170 + 1
                    column = (i % 170) // 10 + 1
                    positions.append((row, column))
            return positions

        # テスト用の数列
        sequence_to_find = number

        # 任意の数列が出現する位置を検索
        positions = find_sequence(sequence_to_find, pi_decimal)

        # 結果を表示
        if positions:
            print(f"The sequence {sequence_to_find} is found at the following positions:")
            # for position in positions:
            #     print(position)
            results = positions
            return jsonify({'results': results})
        else:
            # print(f"The sequence {sequence_to_find} is not found.")
            return jsonify({'results': 'not found'})
    
    except ValueError:
        return jsonify({'results': ['Invalid input']})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
