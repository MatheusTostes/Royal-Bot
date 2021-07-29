from model.locationProject import LocationProject
from model.loginSheets import Login
from model.getSellers import GetSellers
from model.getClients import GetClients
from accounts.sellerData import SellerData
from accounts.validSeller import ValidSeller
from accounts.setVersion import SetVersion

from utils.hourLogin import HourLogin
from view.header import Header


class application():
    try:
        Header()
        location = LocationProject()
        planilha, gc = Login(location)
        dfSellers = GetSellers(planilha)
        login = str(input("Usuario vendedor: "))
        password = str(input("Senha vendedor: "))
        horas = HourLogin()
        valid, state, ExpireDate, Business, user, Online, id, macSeller, phoneSeller = SellerData(
            login, password, dfSellers)
        x = ValidSeller(valid, state, macSeller, Online, user, Business, ExpireDate, gc)
        SetVersion(id, gc)

        print(x)
        # GetClients(planilha, NomeAba)
    except Exception as e:
        print(e)


app = application
