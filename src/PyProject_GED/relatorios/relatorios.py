from reportlab.lib.units                import cm
from reportlab.lib.enums                import TA_CENTER, TA_RIGHT
        
from PyProject_GED.relatorios.base      import Report, ReportBand
from PyProject_GED.relatorios.widgets   import Label, ObjectValue, SystemField
from PyProject_GED.relatorios.utils     import FIELD_ACTION_COUNT, BAND_WIDTH

from PyProject_GED                      import oControle

class estadoUsuarios(Report):
    title = 'Estado dos Usuarios (Ativo/Inativo)'

    class band_begin(ReportBand):
        try :
            height = 1*cm
            elements = [
                Label(text='Lista de Usuarios', top=0.1*cm,
                    left=8*cm),
            ]
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel relatorios - band_begin: ' + str(e))

    class band_page_header(ReportBand):
        try :
            height = 1.3*cm
            elements = [
                SystemField(expression='%(report_title)s', top=0.1*cm,
                    left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold',
                    'fontSize': 14, 'alignment': TA_CENTER}),
                Label(text="Primeiro Nome", top=0.8*cm, left=0*cm),
                Label(text="Ultimo Nome", top=0.8*cm, left=4*cm),
                Label(text="E-mail", top=0.8*cm, left=8*cm),
                Label(text="Ativo", top=0.8*cm, left=15*cm),
            ]
            borders = {'bottom': True}
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel relatorios - band_page_header: ' + str(e))
        
    class band_detail(ReportBand):
        try :
            height = 0.5*cm
            elements = [
                ObjectValue(attribute_name='first_name', top=0, left=0*cm, width=4*cm),
                ObjectValue(attribute_name='last_name', top=0, left=4*cm, width=4*cm),
                ObjectValue(attribute_name='email', top=0, left=8*cm, width=7*cm),
                ObjectValue(attribute_name='is_active', top=0, left=15*cm, width=3*cm,
                            get_value=lambda instance: instance.is_active and 'Sim' or 'Nao'),
            ]
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel relatorios - band_detail: ' + str(e))
            
    class band_summary(ReportBand):
        try :
            height = 0.7*cm
            elements = [
                Label(text="Total", top=0.1*cm, left=0),
                ObjectValue(attribute_name='first_name', top=0.1*cm, left=3*cm,
                    action=FIELD_ACTION_COUNT,
                    display_format='%s usuarios'),
            ]
            borders = {'all': True}
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel relatorios - band_summary: ' + str(e))
            
    class band_page_footer(ReportBand):
        try :
            height = 0.5*cm
            elements = [
                Label(text='Shift IT', top=0.5*cm, left=0),
                SystemField(expression='Pagina # %(page_number)d of %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
            borders = {'top': True}
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel relatorios - band_page_footer: ' + str(e))


class ultimosAcessos(Report):
    title = 'Ultimos Acessos de cada Usuario'

    class band_begin(ReportBand):
        try :
            height = 1*cm
            elements = [
                Label(text='Ultimos Acessos', top=0.1*cm,
                    left=8*cm),
            ]
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel relatorios - band_begin: ' + str(e))

    class band_page_header(ReportBand):
        try :
            height = 1.3*cm
            elements = [
                SystemField(expression='%(report_title)s', top=0.1*cm,
                    left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold',
                    'fontSize': 14, 'alignment': TA_CENTER}),
                Label(text="Primeiro Nome", top=0.8*cm, left=0*cm),
                Label(text="Ultimo Nome", top=0.8*cm, left=4*cm),
                Label(text="E-mail", top=0.8*cm, left=8*cm),
                Label(text="Ultimo Login", top=0.8*cm, left=15*cm),
            ]
            borders = {'bottom': True}
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel relatorios - band_page_header: ' + str(e))
        
    class band_detail(ReportBand):
        try :
            height = 0.5*cm
            elements = [
                ObjectValue(attribute_name='first_name', top=0, left=0*cm, width=4*cm),
                ObjectValue(attribute_name='last_name', top=0, left=4*cm, width=4*cm),
                ObjectValue(attribute_name='email', top=0, left=8*cm, width=5*cm),
                ObjectValue(attribute_name='last_login', top=0, left=15*cm, width=5*cm),
            ]
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel relatorios - band_detail: ' + str(e))

    class band_summary(ReportBand):
        try :
            height = 0.7*cm
            elements = [
                Label(text="Total", top=0.1*cm, left=0),
                ObjectValue(attribute_name='first_name', top=0.1*cm, left=3*cm,
                    action=FIELD_ACTION_COUNT,
                    display_format='%s usuarios'),
            ]
            borders = {'all': True}
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel relatorios - band_summary: ' + str(e))
            
    class band_page_footer(ReportBand):
        try :
            height = 0.5*cm
            elements = [
                Label(text='Shift IT', top=0.1*cm, left=0),
                SystemField(expression='Page # %(page_number)d of %(page_count)d', top=0.1*cm,
                    width=BAND_WIDTH, style={'alignment': TA_RIGHT}),
            ]
            borders = {'top': True}
        except Exception, e:
            oControle.getLogger().error('Nao foi possivel relatorios - band_page_footer: ' + str(e))
