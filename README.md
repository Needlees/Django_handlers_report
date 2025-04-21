<p><b>CLI-приложение для анализа логов Django.</b> <br>Формирует отчет и выводит его в консоль.</p>
<p>python3 main.py [file lists] [--report report name]</p>
<p>Опции:</p>
<ul>
<li>file lists: список лог-файлов</li>
<li>--report report name: где report name - наименование отчета.</li>
</ul>
<p>Пример:<br>
python3 main.py logs/app1.log logs/app2.log logs/app3.log --report handlers
</p>
<p>На текущий момент реализован отчет с наименованием - <i>handlers</i></p>
<p>
<img src="https://github.com/Needlees/Django_handlers_report/blob/master/img/example.png" width="525" style="max-width: 100%">
</p>
<p>Для добавления нового отчета необходимо импортировать модуль с отчетом в <code>main.py</code><br>
и добавить его наименование и функцию по формированию в нижеприведенный словарь:</p>
<pre>
REPORTS: Final[dict[str, Any]] = {
    'handlers': handlers_report
}
</pre>