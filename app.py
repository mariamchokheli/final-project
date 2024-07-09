from ext import app

if __name__=="__main__":
  from routes import register, login, second, product, index, create_product, delete_product, edit_product,delete_comment
  app.run(debug=True)