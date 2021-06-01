class Test:
    test_name = None
    result = False
    error = None
    error_page = None

    def __init__(self):
        return

    def get_test_name(self):
        return self.test_name

    def set_test_name(self, t_n):
        self.test_name = t_n

    def get_result(self):
        return self.result

    def set_result(self, result):
        self.result = result

    def get_error(self):
        return self.error

    def set_error(self, e):
        self.error = e

    def get_error_page(self):
        return self.error_page

    def set_error_page(self, e_p):
        self.error_page = e_p



    def __str__(self):
        return "Test name is: {}\nTest result is: {}\nTest error is: {}\nTest error page is: {}\n".format(
        self.test_name,
        self.result,
        self.get_error(),
        self.get_error_page())


    def __str__direct(self):
        print('Test name is', self.test_name)
        print('Test result is', self.result)
        print('Test error is', self.get_error())
        print('Test error page is', self.get_error_page())
        print('---------------------------------')
        return